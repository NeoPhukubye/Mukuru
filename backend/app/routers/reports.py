"""Report generation endpoints (JSON + PDF)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Response
from sqlmodel import Session, select

from ..config import account_holder_for
from ..db import engine, list_transactions_for_period, trailing_months_range
from ..models import ErrorResponse, ReportResponse, Transaction
from ..routers.credit import summarise_credit_inputs
from ..services.categorizer import category_totals
from ..services.credit_engine import compute_credit_score
from ..services.report_generator import build_report, render_pdf

router = APIRouter(prefix="/generate-financial-report", tags=["reports"])


def _compute_credit(txs: list[Transaction]) -> int:
    """Credit score for a report, using the same inputs as /calculate-credit-score."""
    if not txs:
        return 0
    data = summarise_credit_inputs(txs)
    tenure = data["tenure_months"]
    score, _, _, _ = compute_credit_score(
        user_id="",
        remittance_months=data["remittance_months"],
        total_months=tenure,
        remittance_amounts=data["remittance_amounts"],
        late_months=data["late_months"],
        tenure_months=tenure,
        savings_rate=data["savings_rate"],
    )
    return score


def _build(user_id: str) -> ReportResponse:
    start, end = trailing_months_range(12)
    txs = list_transactions_for_period(user_id, start, end)
    if not txs:
        raise HTTPException(
            status_code=400,
            detail={"error": "no_data", "detail": "No transactions found for this user."},
        )
    return build_report(
        user_id=user_id,
        account_holder=account_holder_for(user_id),
        transactions=txs,
        credit_score=_compute_credit(txs),
        period_months=12,
    )


@router.get("", response_model=ReportResponse, responses={400: {"model": ErrorResponse}})
def generate_report(user_id: str = Query(..., min_length=1, max_length=64)) -> ReportResponse:
    return _build(user_id)


@router.get("/pdf", responses={400: {"model": ErrorResponse}})
def generate_report_pdf(
    user_id: str = Query(..., min_length=1, max_length=64),
) -> Response:
    report = _build(user_id)
    pdf_bytes = render_pdf(report)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="money-coach-report-{user_id}.pdf"',
            "Content-Length": str(len(pdf_bytes)),
        },
    )