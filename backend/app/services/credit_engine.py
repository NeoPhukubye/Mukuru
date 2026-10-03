"""Proprietary credit score engine (300-850). Pure function."""
from __future__ import annotations

from statistics import mean, stdev

from ..models import CreditFactor

SCORE_MIN, SCORE_MAX = 300, 850
SCORE_RANGE = SCORE_MAX - SCORE_MIN

# Factor weights (must sum to 1.0).
WEIGHTS = {
    "remittance_consistency": 0.35,
    "remittance_amount_stability": 0.15,
    "on_time_pattern": 0.15,
    "tenure": 0.10,
    "savings_behavior": 0.25,
}

BANDS = [
    (750, "Excellent"),
    (650, "Very Good"),
    (550, "Good"),
    (450, "Fair"),
    (0, "Poor"),
]


def _band(score: int) -> str:
    for threshold, name in BANDS:
        if score >= threshold:
            return name
    return "Poor"


def _factor_score(raw: float) -> int:
    return max(0, min(100, int(round(raw))))


def _clamp(raw: float) -> float:
    """Clamp a raw factor to 0-100.

    The weighted score used unclamped values while the API reported clamped
    ones, so a consistency factor above 100 inflated the score in a way the
    published breakdown could not explain. Clamp once, use everywhere.
    """
    return max(0.0, min(100.0, raw))


def _remittance_consistency(rem_months: int, total_months: int) -> float:
    if total_months == 0:
        return 0.0
    return (rem_months / total_months) * 100.0


def _amount_stability(amounts: list[float]) -> float:
    if len(amounts) < 2:
        return 100.0
    m = mean(amounts)
    if m == 0:
        return 100.0
    sd = stdev(amounts)
    cv = sd / m
    return max(0.0, 100.0 - cv * 100.0)


def _on_time_pattern(late_months: int, total_months: int) -> float:
    if total_months == 0:
        return 0.0
    return ((total_months - late_months) / total_months) * 100.0


def _tenure_score(months: int) -> float:
    return min(100.0, months * (100.0 / 24.0))


def _savings_score(savings_rate: float) -> float:
    return min(100.0, savings_rate * 100.0 * 2.0)


def compute_credit_score(
    user_id: str,
    remittance_months: int,
    total_months: int,
    remittance_amounts: list[float],
    late_months: int,
    tenure_months: int,
    savings_rate: float,
) -> tuple[int, str, list[CreditFactor], list[str]]:
    """Return (score, band, factors, tips)."""
    raw = {
        "remittance_consistency": _clamp(_remittance_consistency(remittance_months, total_months)),
        "remittance_amount_stability": _clamp(_amount_stability(remittance_amounts)),
        "on_time_pattern": _clamp(_on_time_pattern(late_months, total_months)),
        "tenure": _clamp(_tenure_score(tenure_months)),
        "savings_behavior": _clamp(_savings_score(savings_rate)),
    }

    details = {
        "remittance_consistency": (
            f"{remittance_months} of {total_months} months had a remittance"
        ),
        "remittance_amount_stability": (
            f"amount variance across {len(remittance_amounts)} remittances"
        ),
        "on_time_pattern": (
            f"{total_months - late_months} of {total_months} remittances on time"
        ),
        "tenure": f"{tenure_months} months of history",
        "savings_behavior": f"savings rate {savings_rate * 100:.0f}%",
    }

    factors = [
        CreditFactor(
            name=name.replace("_", " ").title(),
            weight=WEIGHTS[name],
            score=_factor_score(raw[name]),
            detail=details[name],
        )
        for name in WEIGHTS
    ]

    weighted = sum(raw[n] * WEIGHTS[n] for n in WEIGHTS)
    score = int(round(SCORE_MIN + (weighted / 100.0) * SCORE_RANGE))
    score = max(SCORE_MIN, min(SCORE_MAX, score))

    tips: list[str] = []
    if raw["remittance_consistency"] < 80:
        tips.append("Send at least one remittance every month to build consistency.")
    if raw["remittance_amount_stability"] < 70:
        tips.append("Keep remittance amounts stable — large swings can lower your score.")
    if raw["on_time_pattern"] < 80:
        tips.append("Send remittances early in the month to build an on-time pattern.")
    if raw["savings_behavior"] < 50:
        tips.append("Save a small fixed amount each month to boost savings behaviour.")
    if not tips:
        tips.append("Keep up the great work — your credit profile is strengthening.")

    return score, _band(score), factors, tips