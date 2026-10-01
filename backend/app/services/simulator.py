"""Goal-achievement simulator. Pure function."""
from __future__ import annotations

from datetime import date, timedelta


def simulate(
    weekly_amount: float,
    weeks: int,
    goal_target: float | None = None,
    goal_saved: float = 0.0,
    start_date: date | None = None,
) -> dict:
    """Project balance by month and when a goal is hit."""
    start = start_date or date.today()
    monthly = weekly_amount * 4.345
    balance_by_month: list[dict] = []
    cumulative = 0.0
    goal_hit_date: str | None = None
    goal_remaining: float | None = None

    for m in range(weeks):
        cumulative += weekly_amount
        if (m + 1) % 4 == 0 or m == 0:
            balance_by_month.append(
                {
                    "month": (start + timedelta(days=30 * (len(balance_by_month) + 1))).strftime("%Y-%m"),
                    "balance": round(cumulative, 2),
                }
            )
        if goal_target is not None and goal_hit_date is None:
            if cumulative + goal_saved >= goal_target:
                goal_hit_date = (start + timedelta(days=7 * (m + 1))).isoformat()
                goal_remaining = round(max(0.0, goal_target - goal_saved - cumulative), 2)

    total_saved = round(cumulative, 2)
    difference = round(total_saved, 2)  # vs. no saving = 0

    return {
        "projected_balance_by_month": balance_by_month,
        "goal_hit_date": goal_hit_date,
        "goal_remaining": goal_remaining,
        "difference_vs_no_saving": difference,
        "projected_total_saved": total_saved,
    }