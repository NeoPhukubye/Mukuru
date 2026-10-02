"""Coach chat: intent routing with grounded answers, optional Gemini hook,
and a rule-based fallback that works offline.

Model note: `gemini-2.0-flash` was retired by Google on 1 June 2026, so every
request to it failed and silently fell through to the fallback. The default is
now `gemini-3.5-flash`.
"""
from __future__ import annotations

import logging
import os
import re

from ..models import CoachChatResponse

logger = logging.getLogger("moneycoach")

# Gemini configuration. Set GEMINI_API_KEY to enable LLM-backed replies;
# otherwise the rule-based fallback is used (works fully offline).
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
GEMINI_TIMEOUT = float(os.environ.get("GEMINI_TIMEOUT", "20"))


INTENTS = {
    "budget": [
        "budget", "spend", "spending", "saving", "savings rate", "surplus",
        "deficit", "analyze", "earn", "salary", "income", "make",
    ],
    "goal": [
        "goal", "school", "fridge", "target", "progress", "deadline",
        "car", "buy", "save up", "purchase", "house",
    ],
    "simulate": [
        "simulate", "what if", "project", "how much", "weeks", "weekly",
        "a week", "save", "put away", "saving r",
    ],
    "credit": ["credit", "score", "credit score", "improve", "rating"],
    "report": ["report", "pdf", "statement", "summary", "document"],
}


def _classify(message: str) -> str:
    m = message.lower()
    scores = {k: sum(1 for kw in v if kw in m) for k, v in INTENTS.items()}
    best = max(scores, key=scores.get)  # type: ignore[arg-type]
    return best if scores[best] > 0 else "general"


def _context(user_id: str) -> dict:
    """Pull the user's real numbers so replies are grounded, not generic.

    Every part is optional: a user with no transactions still gets a reply.
    """
    from ..db import list_goals
    from ..routers.budget import analyze_budget
    from ..routers.credit import calculate_credit_score
    from ..routers.goals import _progress

    ctx: dict = {}
    try:
        ctx["budget"] = analyze_budget(user_id=user_id)
    except Exception:
        pass
    try:
        ctx["credit"] = calculate_credit_score(user_id=user_id)
    except Exception:
        pass
    try:
        ctx["goals"] = [_progress(g) for g in list_goals(user_id)]
    except Exception:
        pass
    return ctx


def _parse_simulation(message: str) -> tuple[float, int]:
    """Extract 'R100 a week' / '12 weeks' from a message. Defaults 100 / 26."""
    text = message.lower()
    amount = re.search(
        r"r\s?(\d[\d,]*)"
        r"|(\d[\d,]*)\s*(?:rand|per week|a week|/week|weekly)",
        text,
    )
    weeks = re.search(r"(\d+)\s*weeks?", text)

    weekly = float((amount.group(1) or amount.group(2)).replace(",", "")) if amount else 100.0
    if weekly <= 0:
        weekly = 100.0
    span = int(weeks.group(1)) if weeks else 26
    return weekly, max(1, min(span, 260))


def _focus_goals(goals: list, message: str) -> list:
    """Prefer goals the user actually named, e.g. 'how's my fridge'."""
    named = [g for g in goals if g.name.lower() in message.lower()]
    return named or goals


def _fallback(message: str, intent: str, ctx: dict) -> tuple[str, list[str]]:
    budget = ctx.get("budget")
    credit = ctx.get("credit")
    goals = ctx.get("goals") or []
    focus = _focus_goals(goals, message)

    if intent == "budget" and budget:
        detail = budget.insights[1] if len(budget.insights) > 1 else ""
        reply = (
            f"This month you've brought in R{budget.total_income:,.0f} and spent "
            f"R{budget.total_expenses:,.0f}, leaving R{budget.surplus_deficit:,.0f} "
            f"— a {budget.savings_rate * 100:.0f}% savings rate."
        )
        if detail:
            reply += " " + detail
        return reply, ["Simulate R100/week", "Check my goals"]

    if intent == "goal":
        lower_msg = message.lower()
        # A named asset the user does not already track: answer about *that*
        # item instead of listing unrelated goals.
        new_asset = next((a for a in ("car", "house") if a in lower_msg and a not in
                          {g.name.lower() for g in goals}), None)
        if new_asset:
            income = budget.total_income if budget else 12000.0
            monthly = income * 0.15
            months = 6
            reply = (
                f"Saving for a {new_asset} is a great milestone, Grace! With your "
                f"R{income:,.0f} monthly income, putting aside about 15% "
                f"(R{monthly:,.0f}/month) would build a down payment in about "
                f"{months} months. "
                f"Would you like me to add '{new_asset.title()}' as a new savings goal?"
            )
            return reply, [
                f"Yes, add {new_asset.title()} goal",
                "Simulate R500/week",
                "Check my budget",
            ]

        if focus:
            return (
                " ".join(g.nudge for g in focus[:2]),
                ["Simulate R100/week", "Analyze my budget"],
            )

    if intent == "credit" and credit:
        return (
            f"Your credit score is {credit.score} ({credit.band}). {credit.tips[0]}",
            ["Generate my report", "Check my goals"],
        )

    if intent == "simulate":
        from .simulator import simulate

        weekly, weeks = _parse_simulation(message)
        goal = focus[0] if focus else None
        result = simulate(
            weekly,
            weeks,
            goal_target=goal.target_amount if goal else None,
            goal_saved=goal.saved_amount if goal else 0.0,
        )
        reply = (
            f"Saving R{weekly:,.0f} a week for {weeks} weeks puts "
            f"R{result['projected_total_saved']:,.0f} aside."
        )
        if goal and result["goal_hit_date"]:
            reply += f" You'd finish your {goal.name} goal around {result['goal_hit_date']}."
        elif goal:
            reply += f" That is not enough to finish {goal.name} in that time — try a higher amount."
        return reply, ["Simulate R200/week", "Check my goals"]

    if intent == "report":
        return (
            "I can generate a downloadable PDF with your income, spending and "
            "credit score — tap below.",
            ["Generate my report"],
        )

    return (
        "Hi! I'm your Money Coach. Ask me about your budget, savings goals, "
        'a what-if like "save R100 a week", or your credit score.',
        ["Analyze budget", "Check goals", "Simulate R100/week", "Credit score"],
    )


def _facts(ctx: dict) -> str:
    lines: list[str] = []
    budget = ctx.get("budget")
    credit = ctx.get("credit")

    if budget:
        lines.append(
            f"This month: income R{budget.total_income:,.0f}, "
            f"expenses R{budget.total_expenses:,.0f}, "
            f"surplus R{budget.surplus_deficit:,.0f}, "
            f"savings rate {budget.savings_rate * 100:.0f}%."
        )
    if credit:
        lines.append(f"Credit score {credit.score} ({credit.band}).")
    for g in ctx.get("goals") or []:
        lines.append(
            f"Goal {g.name}: R{g.saved_amount:,.0f} of R{g.target_amount:,.0f} "
            f"({g.percent_complete}%), due {g.deadline}."
        )
    return "\n".join(lines)


def _gemini_chat(user_id: str, message: str, ctx: dict) -> CoachChatResponse:
    """Optional Gemini hook via the REST API. Never called without a key."""
    import httpx

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    system = (
        "You are a friendly Money Coach for a remittance user in South Africa. "
        "Be concise (max 3 short sentences), warm and jargon-free. Use Rands (R). "
        "Plain text only: no markdown, no asterisks, no bullet points. "
        "Never give binding financial advice. "
        "Answer using ONLY these facts about the user when relevant:\n" + _facts(ctx)
    )

    resp = httpx.post(
        url,
        # Send the key in a header rather than the query string so it cannot
        # end up in proxy or access logs.
        headers={"x-goog-api-key": GEMINI_API_KEY},
        json={
            "contents": [{"role": "user", "parts": [{"text": message}]}],
            "systemInstruction": {"parts": [{"text": system}]},
        },
        timeout=GEMINI_TIMEOUT,
    )
    resp.raise_for_status()
    reply = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    return CoachChatResponse(
        reply=reply,
        suggested_actions=["Analyze budget", "Check goals", "Credit score"],
    )


def chat(user_id: str, message: str) -> CoachChatResponse:
    intent = _classify(message)
    ctx = _context(user_id)

    if GEMINI_API_KEY:
        try:
            return _gemini_chat(user_id, message, ctx)
        except Exception as exc:
            # Never fail the demo, but never fail silently either: a dead key,
            # a retired model, or an exhausted quota all land here.
            logger.warning("Gemini call failed, using fallback: %s", exc)

    reply, actions = _fallback(message, intent, ctx)
    return CoachChatResponse(reply=reply, suggested_actions=actions)