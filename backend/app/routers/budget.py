"""Budget analysis endpoint."""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from ..db import engine
from ..models import BudgetAnalysis, ErrorResponse, Transaction
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

    top = max(totals.items(), key=lambda kv: abs(kv[1])) if totals else ("other", 0.0)
    if top[0] != "remittance" and abs(top[1]) > 0:
        insights.append(f"Your biggest outflow is {top[0]} at R{abs(top[1]):,.0f} — worth keeping an eye on.")
    else:
        insights.append("Your remittances are your biggest commitment — keeping them consistent builds trust and credit.")

    if expenses > income:
        insights.append("Consider setting a small weekly spending cap to stay in the green.")
    else:
        insights.append(f"You have a R{income - expenses:,.0f} surplus — great raw material for your goals.")
    return insights[:3]


@router.get("", response_model=BudgetAnalysis, responses={400: {"model": ErrorResponse}})
def analyze_budget(
    user_id: str = Query(..., min_length=1, max_length=64),
) -> BudgetAnalysis:
    with Session(engine) as session:
        txs = list(session.exec(select(Transaction).where(Transaction.user_id == user_id)).all())

    if not txs:
        raise HTTPException(
            status_code=400,
            detail={"error": "no_data", "detail": "No transactions found for this user."},
        )

    totals = category_totals(txs)
    income = round(sum(t.amount for t in txs if t.type == "credit"), 2)
    expenses = round(sum(t.amount for t in txs if t.type == "debit"), 2)
    surplus = round(income - expenses, 2)
    rate = round(max(0.0, surplus) / income, 4) if income > 0 else 0.0

    return BudgetAnalysis(
        user_id=user_id,
        month=date.today().strftime("%Y-%m"),
        totals_by_category={k: round(v, 2) for k, v in totals.items()},
        total_income=income,
        total_expenses=expenses,
        savings_rate=rate,
        surplus_deficit=surplus,
        insights=_insights(totals, income, expenses, rate),
    )