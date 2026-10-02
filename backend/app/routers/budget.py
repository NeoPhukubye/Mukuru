"""Budget analysis endpoint."""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from ..db import current_month_range, list_transactions, list_transactions_for_period
from ..models import BudgetAnalysis, ErrorResponse
from ..services.categorizer import category_totals

router = APIRouter(prefix="/analyze-budget", tags=["budget"])


def _insights(totals: dict[str, float], income: float, expenses: float, rate: float) -> list[str]:
    insights: list[str] = []
    if rate >= 0.20:
        insights.append(f"You're saving {rate * 100:.0f}% of your income — that's excellent momentum.")
    elif rate >= 0.10:
        insights.append(f"You're saving {rate * 100:.0f}% of your income. Steady and healthy.")
    elif rate > 0:
        insights.append(f"You're saving only {rate * 100:.0f}% of your income. Let's find some wiggle room.")
    else:
        insights.append("You're spending more than you earn this month. Small cuts can help turn this around.")

    # Only consider genuine outflows. Ranking by absolute value across signed
    # totals used to report a large salary credit as the biggest expense.
    outflows = {cat: amount for cat, amount in totals.items() if amount < 0}
    if outflows:
        # Most negative total == largest outflow.
        top_cat, top_amount = min(outflows.items(), key=lambda kv: kv[1])
        if top_cat == "remittance":
            insights.append("Your remittances are your biggest commitment — keeping them consistent builds trust and credit.")
        else:
            insights.append(f"Your biggest outflow is {top_cat} at R{abs(top_amount):,.0f} — worth keeping an eye on.")
    else:
        insights.append("You have no spending recorded this month — everything came in as income.")

    if expenses > income:
        insights.append("Consider setting a small weekly spending cap to stay in the green.")
    else:
        insights.append(f"You have a R{income - expenses:,.0f} surplus — great raw material for your goals.")
    return insights[:3]


@router.get("", response_model=BudgetAnalysis, responses={400: {"model": ErrorResponse}})
def analyze_budget(
    user_id: str = Query(..., min_length=1, max_length=64),
) -> BudgetAnalysis:
    """Analyse the current calendar month only.

    Earlier versions summed a user's entire history and reported it under the
    current month, which inflated every figure by the length of the record.
    """
    start, end = current_month_range()
    txs = list_transactions_for_period(user_id, start, end)

    if not txs:
        # Early in a new month there may be nothing yet. Falling back to the
        # latest month that has data keeps the dashboard populated instead of
        # rendering a 400, which is what the frontend shows on empty state.
        past = [t for t in list_transactions(user_id) if t.date <= date.today()]
        if past:
            start, end = current_month_range(max(t.date for t in past))
            txs = list_transactions_for_period(user_id, start, end)

    if not txs:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "no_data",
                "detail": f"No transactions found for this user in {start.strftime('%Y-%m')}.",
            },
        )

    totals = category_totals(txs)
    income = round(sum(t.amount for t in txs if t.type == "credit"), 2)
    expenses = round(sum(t.amount for t in txs if t.type == "debit"), 2)
    surplus = round(income - expenses, 2)
    rate = round(max(0.0, surplus) / income, 4) if income > 0 else 0.0

    return BudgetAnalysis(
        user_id=user_id,
        month=start.strftime("%Y-%m"),
        totals_by_category={k: round(v, 2) for k, v in totals.items()},
        total_income=income,
        total_expenses=expenses,
        savings_rate=rate,
        surplus_deficit=surplus,
        insights=_insights(totals, income, expenses, rate),
    )