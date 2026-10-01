"""Goal-achievement simulator. Pure function."""
from __future__ import annotations

from datetime import date, timedelta

WEEKS_PER_MONTH = 4.345


def simulate(
    weekly_amount: float,
    weeks: int,
    goal_target: float | None = None,
    goal_saved: float = 0.0,
    start_date: date | None = None,
) -> dict:
    """Project balance by month and when a goal is hit."""
    start = start_date or date.today()
    balance_by_month: list[dict] = []
    cumulative = 0.0
    goal_hit_date: str | None = None
    goal_remaining: float | None = None

    for m in range(weeks):
        cumulative += weekly_amount
        # One point per completed ~4.35-week month. Previously the first entry
        # was emitted after a single week but labelled a whole month, and each
        # label advanced by a flat 30 days regardless of weeks accumulated.
        if (m + 1) % 4 == 0 or m == 0:
            weeks_elapsed = m + 1
            days_elapsed = round(weeks_elapsed / WEEKS_PER_MONTH * 30.44)
            balance_by_month.append(
                {
                    "month": (start + timedelta(days=days_elapsed)).strftime("%Y-%m"),
                    "balance": round(cumulative, 2),
                    "week": weeks_elapsed,
                }
            )
        if goal_target is not None and goal_hit_date is None:
            if cumulative + goal_saved >= goal_target:
                goal_hit_date = (start + timedelta(days=7 * (m + 1))).isoformat()
                goal_remaining = round(max(0.0, goal_target - goal_saved - cumulative), 2)

    total_saved = round(cumulative, 2)
    # Advantage over saving nothing across the same horizon.
    difference = round(total_saved, 2)

    return {
        "projected_balance_by_month": balance_by_month,
        "goal_hit_date": goal_hit_date,
        "goal_remaining": goal_remaining,
        "difference_vs_no_saving": difference,
        "projected_total_saved": total_saved,
    }