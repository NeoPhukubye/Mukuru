"""Advisory engine endpoint."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from ..db import current_month_range, list_transactions_for_period
from ..models import AdviceResponse, ErrorResponse
from ..services.advisor import advise as _advise

router = APIRouter(prefix="/advice", tags=["advice"])


@router.get("", response_model=AdviceResponse, responses={400: {"model": ErrorResponse}})
def advice(
    user_id: str = Query(..., min_length=1, max_length=64),
) -> AdviceResponse:
    """Advise on the current calendar month only.

    The figures below are monthly, so they must not accumulate history —
    doing so produced injections 12x too large for a year of seeded data.
    """
    start, end = current_month_range()
    txs = list_transactions_for_period(user_id, start, end)
    if not txs:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "no_data",
                "detail": f"No transactions found for this user in {start.strftime('%Y-%m')}.",
            },
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