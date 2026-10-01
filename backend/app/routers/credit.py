"""Credit score endpoint."""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from ..db import list_transactions_for_period, trailing_months_range
from ..models import CreditScoreResponse, ErrorResponse, Transaction
from ..services.credit_engine import compute_credit_score

router = APIRouter(prefix="/calculate-credit-score", tags=["credit"])


def summarise_credit_inputs(txs: list[Transaction]) -> dict[str, Any]:
    """Derive credit inputs from a transaction list.

    Shared with the reports router so both endpoints return identical scores.
    Each used to count remittances differently (transactions vs distinct
    months), so the same user got two different numbers depending on which
    endpoint was called.
    """
    if not txs:
        raise ValueError("no transactions")

    ordered = sorted(txs, key=lambda t: t.date)
    start, end = ordered[0].date, ordered[-1].date

    # Distinct calendar months containing at least one remittance. Counting
    # transactions instead let two remittances in one month push consistency
    # above 100%.
    remittance_dates: list[date] = [t.date for t in ordered if t.is_remittance]
    remittance_months = len({d.strftime("%Y-%m") for d in remittance_dates})
    remittance_amounts = [t.amount for t in ordered if t.is_remittance]

    # A month counts as late only if its latest remittance went past the 25th.
    last_in_month: dict[str, date] = {}
    for d in remittance_dates:
        key = d.strftime("%Y-%m")
        if key not in last_in_month or d > last_in_month[key]:
            last_in_month[key] = d
    late_months = sum(1 for d in last_in_month.values() if d.day > 25)

    tenure_months = max(1, (end.year - start.year) * 12 + (end.month - start.month) + 1)

    income = sum(t.amount for t in ordered if t.type == "credit")
    expenses = sum(t.amount for t in ordered if t.type == "debit")
    savings_rate = max(0.0, income - expenses) / income if income > 0 else 0.0

    return {
        "start": start,
        "end": end,
        "remittance_months": remittance_months,
        "remittance_amounts": remittance_amounts,
        "late_months": late_months,
        "tenure_months": tenure_months,
        "savings_rate": savings_rate,
    }


@router.get("", response_model=CreditScoreResponse, responses={400: {"model": ErrorResponse}})
def calculate_credit_score(
    user_id: str = Query(..., min_length=1, max_length=64),
) -> CreditScoreResponse:
    """Score over the trailing 12 months, matching the financial report window."""
    start, end = trailing_months_range(12)
    txs = list_transactions_for_period(user_id, start, end)

    if not txs:
        raise HTTPException(
            status_code=400,
            detail={"error": "no_data", "detail": "No transactions found for this user."},
        )

    data = summarise_credit_inputs(txs)
    start = data["start"]
    tenure_months = data["tenure_months"]

    score, band, factors, tips = compute_credit_score(
        user_id=user_id,
        remittance_months=data["remittance_months"],
        total_months=tenure_months,
        remittance_amounts=data["remittance_amounts"],
        late_months=data["late_months"],
        tenure_months=tenure_months,
        savings_rate=data["savings_rate"],
    )

    # Deterministic history: interpolate from 300 up to the final score.
    history: list[dict] = []
    month_date = date(start.year, start.month, 1)
    for i in range(tenure_months):
        t = (i + 1) / tenure_months
        history.append({"month": month_date.strftime("%Y-%m"), "score": int(round(300 + t * (score - 300)))})
        month_date = (month_date.replace(day=28) + timedelta(days=4)).replace(day=1)

    return CreditScoreResponse(
        user_id=user_id,
        score=score,
        band=band,
        factors=factors,
        tips=tips,
        history=history,
    )