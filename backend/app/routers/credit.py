"""Credit score endpoint."""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from ..db import engine
from ..models import CreditScoreResponse, ErrorResponse, Transaction
from ..services.credit_engine import compute_credit_score

router = APIRouter(prefix="/calculate-credit-score", tags=["credit"])


@router.get("", response_model=CreditScoreResponse, responses={400: {"model": ErrorResponse}})
def calculate_credit_score(
    user_id: str = Query(..., min_length=1, max_length=64),
) -> CreditScoreResponse:
    with Session(engine) as session:
        txs = list(session.exec(select(Transaction).where(Transaction.user_id == user_id)).all())

    if not txs:
        raise HTTPException(
            status_code=400,
            detail={"error": "no_data", "detail": "No transactions found for this user."},
        )

    txs_sorted = sorted(txs, key=lambda t: t.date)
    start = txs_sorted[0].date
    end = txs_sorted[-1].date

    remittance_amounts: list[float] = []
    remittance_months = 0
    late_months = 0
    last_remit: dict[str, date] = {}

    for t in txs:
        if t.is_remittance:
            remittance_amounts.append(t.amount)
            mk = t.date.strftime("%Y-%m")
            remittance_months += 1
            last_remit[mk] = t.date

    for d in last_remit.values():
        if d.day > 25:
            late_months += 1

    # Tenure in months from first to last transaction.
    tenure_months = max(1, (end.year - start.year) * 12 + (end.month - start.month) + 1)

    income = sum(t.amount for t in txs if t.type == "credit")
    expenses = sum(t.amount for t in txs if t.type == "debit")
    surplus = income - expenses
    savings_rate = max(0.0, surplus) / income if income > 0 else 0.0

    score, band, factors, tips = compute_credit_score(
        user_id=user_id,
        remittance_months=remittance_months,
        total_months=tenure_months,
        remittance_amounts=remittance_amounts,
        late_months=late_months,
        tenure_months=tenure_months,
        savings_rate=savings_rate,
    )

    # Deterministic history: interpolate from 300 up to the final score.
    from datetime import timedelta as _td

    history: list[dict] = []
    month_date = date(start.year, start.month, 1)
    for i in range(tenure_months):
        t = (i + 1) / tenure_months
        history.append({"month": month_date.strftime("%Y-%m"), "score": int(round(300 + t * (score - 300)))})
        month_date = (month_date.replace(day=28) + _td(days=4)).replace(day=1)

    return CreditScoreResponse(
        user_id=user_id,
        score=score,
        band=band,
        factors=factors,
        tips=tips,
        history=history,
    )