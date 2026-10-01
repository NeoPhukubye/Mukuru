"""Report generation endpoints (JSON + PDF)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Response
from sqlmodel import Session, select

from ..db import engine
from ..models import ErrorResponse, ReportResponse, Transaction
from ..services.categorizer import category_totals
from ..services.credit_engine import compute_credit_score
from ..services.report_generator import build_report, render_pdf

router = APIRouter(prefix="/generate-financial-report", tags=["reports"])

USER_NAMES = {"grace": "Grace Moyo"}


def _compute_credit(user_id: str) -> int:
    with Session(engine) as session:
        txs = list(session.exec(select(Transaction).where(Transaction.user_id == user_id)).all())
    if not txs:
        return 0
    txs_sorted = sorted(txs, key=lambda t: t.date)
    start, end = txs_sorted[0].date, txs_sorted[-1].date
    rem_amounts = [t.amount for t in txs if t.is_remittance]
    rem_months = len(rem_amounts)
    late = sum(1 for t in txs if t.is_remittance and t.date.day > 25)
    tenure = max(1, (end.year - start.year) * 12 + (end.month - start.month) + 1)
    income = sum(t.amount for t in txs if t.type == "credit")
    expenses = sum(t.amount for t in txs if t.type == "debit")
    rate = max(0.0, income - expenses) / income if income > 0 else 0.0
    score, _, _, _ = compute_credit_score(
        user_id=user_id,
        remittance_months=rem_months,
        total_months=tenure,
        remittance_amounts=rem_amounts,
        late_months=late,
        tenure_months=tenure,
        savings_rate=rate,
    )
    return score


def _build(user_id: str) -> ReportResponse:
    with Session(engine) as session:
        txs = list(session.exec(select(Transaction).where(Transaction.user_id == user_id)).all())
    if not txs:
        raise HTTPException(
            status_code=400,
            detail={"error": "no_data", "detail": "No transactions found for this user."},
        )
    return build_report(
        user_id=user_id,
        account_holder=USER_NAMES.get(user_id, user_id.title()),
        transactions=txs,
        credit_score=_compute_credit(user_id),
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