"""Advisory engine endpoint."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from ..db import engine
from ..models import AdviceResponse, ErrorResponse, Transaction
from ..services.advisor import advise as _advise

router = APIRouter(prefix="/advice", tags=["advice"])


@router.get("", response_model=AdviceResponse, responses={400: {"model": ErrorResponse}})
def advice(
    user_id: str = Query(..., min_length=1, max_length=64),
) -> AdviceResponse:
    with Session(engine) as session:
        txs = list(session.exec(select(Transaction).where(Transaction.user_id == user_id)).all())
    if not txs:
        raise HTTPException(
            status_code=400,
            detail={"error": "no_data", "detail": "No transactions found for this user."},
        )

    monthly_income = round(sum(t.amount for t in txs if t.type == "credit"), 2)
    monthly_expenses = round(sum(t.amount for t in txs if t.type == "debit"), 2)
    monthly_remittance = round(sum(t.amount for t in txs if t.is_remittance), 2)

    return _advise(
        user_id=user_id,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        monthly_remittance=monthly_remittance,
        existing_emergency=0.0,
    )