"""PDF + JSON report generation. Pure functions for data, I/O for PDF."""
from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timezone

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from ..models import ReportResponse
from ..services.categorizer import category_totals


def build_report(
    user_id: str,
    account_holder: str,
    transactions: Iterable,
    credit_score: int,
    period_months: int = 12,
    generated_at: datetime | None = None,
) -> ReportResponse:
    txs = list(transactions)
    totals = category_totals(txs)

    total_income = round(sum(t.amount for t in txs if t.type == "credit"), 2)
    total_remittances = round(
        sum(t.amount for t in txs if t.is_remittance), 2
    )
    rem_months = len({t.date.strftime("%Y-%m") for t in txs if t.is_remittance})
    avg_rem = round(total_remittances / rem_months, 2) if rem_months else 0.0

    breakdown = [
        {"category": cat, "total": round(val, 2), "count": sum(1 for t in txs if t.category == cat)}
        for cat, val in sorted(totals.items(), key=lambda kv: -kv[1])
    ]

    return ReportResponse(
        user_id=user_id,
        account_holder=account_holder,
        generated_at=generated_at or datetime.now(timezone.utc),
        period_months=period_months,
        income_summary={
            "total_income": total_income,
            "total_remittances": total_remittances,
            "remittance_months": rem_months,
            "average_monthly_remittance": avg_rem,
        },
        category_breakdown=breakdown,
        credit_score=credit_score,
        disclaimer=(
            "This report is for informational purposes only and does not constitute "
            "financial advice. Data is illustrative and based on user-provided transactions."
        ),
    )


def render_pdf(report: ReportResponse) -> bytes:
    """Render a ReportResponse to PDF bytes using reportlab."""
    from io import BytesIO

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    y = height - 20 * mm
    c.setFont("Helvetica-Bold", 18)
    c.drawString(20 * mm, y, "Money Coach — Financial Report")
    y -= 10 * mm
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, y, f"Account holder: {report.account_holder}")
    y -= 6 * mm
    c.drawString(20 * mm, y, f"Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M')}")
    y -= 6 * mm
    c.drawString(20 * mm, y, f"Period: last {report.period_months} months")
    y -= 8 * mm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y, "Income Summary")
    y -= 7 * mm
    c.setFont("Helvetica", 10)
    for k, v in report.income_summary.items():
        c.drawString(25 * mm, y, f"{k}: R{v:,.2f}")
        y -= 5 * mm
    y -= 4 * mm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y, "Category Breakdown")
    y -= 7 * mm
    c.setFont("Helvetica", 10)
    for item in report.category_breakdown:
        c.drawString(
            25 * mm, y,
            f"{item['category']}: R{item['total']:,.2f} ({item['count']} txns)",
        )
        y -= 5 * mm
        if y < 20 * mm:
            c.showPage()
            y = height - 20 * mm
            c.setFont("Helvetica", 10)

    y -= 4 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y, f"Credit Score: {report.credit_score}")
    y -= 8 * mm
    c.setFont("Helvetica", 9)
    c.drawString(20 * mm, y, report.disclaimer)

    c.showPage()
    c.save()
    return buf.getvalue()