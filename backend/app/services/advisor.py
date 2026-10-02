"""Deterministic, rule-based financial advisor."""
from __future__ import annotations

from ..models import AdviceResponse

# Rule config — tweak here to change behaviour.
RULES = {
    "emergency_fund_months": 3,
    "base_monthly_injection_pct": 0.15,  # of net income
    "min_savings_rate": 0.10,
    "pool_weights": {
        "emergency_fund": 0.50,
        "goal_savings": 0.35,
        "investment": 0.15,
    },
    "high_surplus_threshold": 0.30,  # savings rate above this is "high"
    "low_surplus_threshold": 0.05,
}


def _savings_rate(surplus: float, income: float) -> float:
    if income <= 0:
        return 0.0
    return max(0.0, surplus) / income


def advise(
    user_id: str,
    monthly_income: float,
    monthly_expenses: float,
    monthly_remittance: float,
    existing_emergency: float = 0.0,
) -> AdviceResponse:
    """Produce a deterministic advisory from monthly cash-flow numbers."""
    surplus = monthly_income - monthly_expenses
    rate = _savings_rate(surplus, monthly_income)

    if monthly_income <= 0:
        injection = 0.0
        rationale = "We couldn't detect reliable income this month, so we recommend starting small and building up."
    else:
        injection = monthly_income * RULES["base_monthly_injection_pct"]
        if rate < RULES["min_savings_rate"]:
            injection = monthly_income * 0.05
            rationale = (
                f"Your current savings rate is {rate * 100:.0f}%, below our {RULES['min_savings_rate'] * 100:.0f}% floor. "
                f"We recommend a modest injection of R{injection:,.0f}/month so you can build the habit without strain."
            )
        elif rate >= RULES["high_surplus_threshold"]:
            injection = monthly_income * 0.25
            rationale = (
                f"Excellent — you're saving {rate * 100:.0f}% of income. We can push that to R{injection:,.0f}/month "
                f"and accelerate your goals."
            )
        else:
            rationale = (
                f"You're saving {rate * 100:.0f}% of income — a solid position. "
                f"R{injection:,.0f}/month keeps momentum without stress."
            )

    # Adjust weights if emergency fund is short.
    emergency_target = monthly_expenses * RULES["emergency_fund_months"]
    emergency_short = max(0.0, emergency_target - existing_emergency)
    weights = dict(RULES["pool_weights"])
    if emergency_short > 0:
        weights["emergency_fund"] = 0.60
        weights["goal_savings"] = 0.30
        weights["investment"] = 0.10
        rationale += (
            f" A {RULES['emergency_fund_months']}-month emergency fund is about "
            f"R{emergency_target:,.0f}, so we're weighting that pool most heavily."
        )

    pools = [
        {
            "pool": k,
            "amount": round(injection * v, 2),
            "weight": v,
        }
        for k, v in weights.items()
    ]

    return AdviceResponse(
        user_id=user_id,
        monthly_injection=round(injection, 2),
        allocation={p["pool"]: p["amount"] for p in pools},
        rationale=rationale,
        pools=pools,
    )