"""Coach chat: intent routing with optional Gemini LLM hook and rule-based fallback."""
from __future__ import annotations

import os

from ..models import CoachChatResponse

# Gemini configuration. Set GEMINI_API_KEY to enable LLM-backed replies;
# otherwise the rule-based fallback is used (works fully offline).
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_TIMEOUT = float(os.environ.get("GEMINI_TIMEOUT", "10"))


INTENTS = {
    "budget": ["budget", "spend", "spending", "saving", "savings rate", "surplus", "deficit", "analyze"],
    "goal": ["goal", "school", "fridge", "target", "progress", "deadline"],
    "simulate": ["simulate", "what if", "project", "how much", "weeks", "weekly"],
    "credit": ["credit", "score", "credit score", "improve"],
    "report": ["report", "pdf", "statement", "summary"],
}


def _classify(message: str) -> str:
    m = message.lower()
    scores = {k: sum(1 for kw in v if kw in m) for k, v in INTENTS.items()}
    best = max(scores, key=scores.get)  # type: ignore[arg-type]
    return best if scores[best] > 0 else "general"


def _fallback(user_id: str, message: str, intent: str) -> tuple[str, list[str]]:
    actions: list[str] = []
    if intent == "budget":
        reply = (
            "I can break down your spending by category and tell you your savings rate. "
            "Ask me to analyze your budget anytime."
        )
        actions = ["Analyze my budget", "See savings tips"]
    elif intent == "goal":
        reply = (
            "You have savings goals set up. I can tell you how close you are to hitting each one "
            "and nudge you along the way."
        )
        actions = ["View my goals", "Check goal progress"]
    elif intent == "simulate":
        reply = (
            "Tell me how much you want to save each week and for how many weeks, "
            "and I'll project when you'll hit your goal."
        )
        actions = ["Simulate R100/week for 12 weeks", "Simulate R200/week"]
    elif intent == "credit":
        reply = (
            "Your credit score is built from your remittance consistency, amount stability, "
            "on-time pattern, tenure, and savings behaviour. I can show the breakdown."
        )
        actions = ["Check my credit score", "See tips to improve"]
    elif intent == "report":
        reply = "I can generate a downloadable PDF financial report with your income, spending, and credit summary."
        actions = ["Generate my report"]
    else:
        reply = (
            "Hi! I'm your Money Coach. You can ask me about your budget, savings goals, "
            "what-if simulations, or credit score."
        )
        actions = ["Analyze budget", "Check goals", "Simulate savings", "Credit score"]
    return reply, actions


def chat(user_id: str, message: str) -> CoachChatResponse:
    intent = _classify(message)

    if GEMINI_API_KEY:
        try:
            return _gemini_chat(user_id, message, intent)
        except Exception:
            pass  # fall through to rule-based fallback

    reply, actions = _fallback(user_id, message, intent)
    return CoachChatResponse(reply=reply, suggested_actions=actions)


def _gemini_chat(user_id: str, message: str, intent: str) -> CoachChatResponse:
    """Optional Gemini hook via the REST API. Never called without an API key."""
    import httpx

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )
    resp = httpx.post(
        url,
        json={
            "contents": [
                {"role": "user", "parts": [{"text": message}]}
            ],
            "systemInstruction": {
                "parts": [
                    {
                        "text": (
                            "You are a friendly Money Coach for a remittance user in South Africa. "
                            "Be concise, warm, and jargon-free. Use Rands (R) for amounts. "
                            "Never give medical, legal, or binding financial advice."
                        )
                    }
                ]
            },
            "generationConfig": {"temperature": 0.4},
        },
        timeout=GEMINI_TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json()
    reply = data["candidates"][0]["content"]["parts"][0]["text"]
    return CoachChatResponse(reply=reply, suggested_actions=[])