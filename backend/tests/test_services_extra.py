"""Unit tests for the advisory, report, and coach service functions.

These are pure functions with no I/O, so they are trivially testable. They had
no coverage before: only the categoriser, credit engine, and simulator were
exercised by tests/test_services.py.
"""
from __future__ import annotations

from datetime import date, datetime, timezone

from app.models import Transaction
from app.services.advisor import advise
from app.services.report_generator import build_report
from app.services.simulator import simulate as _simulate

# --- advisor -----------------------------------------------------------------

def test_advise_low_savings_rate():
    res = advise(user_id="u", monthly_income=10000.0, monthly_expenses=9500.0,
                 monthly_remittance=2500.0)
    # 5% surplus -> below the 10% floor, so injection drops to 5% of income.
    assert res.monthly_injection == 500.0
    assert res.allocation["emergency_fund"] > 0
    assert "below our" in res.rationale.lower()


def test_advise_high_surplus():
    res = advise(user_id="u", monthly_income=10000.0, monthly_expenses=7000.0,
                 monthly_remittance=2500.0)
    assert res.monthly_injection == 2500.0
    assert "excellent" in res.rationale.lower()


def test_advise_weights_emergency_when_short():
    res = advise(user_id="u", monthly_income=10000.0, monthly_expenses=5000.0,
                 monthly_remittance=2500.0, existing_emergency=0.0)
    # 3 months of expenses is 15000, so the emergency pool gets the extra weight.
    assert res.allocation["emergency_fund"] > res.allocation["investment"]
    assert "emergency fund" in res.rationale.lower()


def test_advise_no_income():
    res = advise(user_id="u", monthly_income=0.0, monthly_expenses=0.0,
                 monthly_remittance=0.0)
    assert res.monthly_injection == 0.0
    assert "starting small" in res.rationale.lower()


def test_advise_pool_weights_sum_to_injection():
    res = advise(user_id="u", monthly_income=10000.0, monthly_expenses=8000.0,
                 monthly_remittance=2500.0)
    total = round(sum(p["amount"] for p in res.pools), 2)
    assert total == res.monthly_injection


# --- report generator --------------------------------------------------------

def _tx(date, amount, tx_type, category, is_rem=False, merchant="M", desc="d"):
    return Transaction(
        id=1, user_id="u", date=date, amount=amount, merchant=merchant,
        description=desc, type=tx_type, category=category, is_remittance=is_rem,
    )


def test_build_report_includes_remittance_summary():
    txs = [
        _tx(date(2026, 1, 5), 2500.0, "debit", "remittance",
             is_rem=True, merchant="Mukuru", desc="Send money home"),
        _tx(date(2026, 1, 1), 8000.0, "credit", "other",
            merchant="Employer", desc="Salary"),
        _tx(date(2026, 1, 3), 720.0, "debit", "groceries",
            merchant="Checkers", desc="Groceries"),
    ]
    report = build_report(user_id="u", account_holder="Grace Moyo",
                          transactions=txs, credit_score=620, period_months=12,
                          generated_at=datetime.now(timezone.utc))
    assert report.account_holder == "Grace Moyo"
    assert report.credit_score == 620
    assert report.income_summary["total_income"] == 8000.0
    assert report.income_summary["total_remittances"] == 2500.0
    assert report.income_summary["remittance_months"] == 1
    assert any(b["category"] == "groceries" for b in report.category_breakdown)
    assert "informational" in report.disclaimer.lower()


def test_build_report_empty_transactions_is_safe():
    report = build_report(user_id="u", account_holder="Grace Moyo",
                          transactions=[], credit_score=0, period_months=12,
                          generated_at=datetime.now(timezone.utc))
    assert report.income_summary["total_income"] == 0
    assert report.category_breakdown == []


# --- simulator integration with a goal ---------------------------------------

def test_simulate_goal_hit_date_is_realistic():
    result = _simulate(weekly_amount=100.0, weeks=52,
                       goal_target=5200.0, goal_saved=0.0,
                       start_date=date(2026, 1, 1))
    assert result["goal_hit_date"] is not None
    # 100/week for 52 weeks = 5200, so the goal is hit at the very end.
    hit = date.fromisoformat(result["goal_hit_date"])
    assert hit <= date(2026, 12, 31)
    assert result["projected_total_saved"] == 5200.0


def test_simulate_no_goal_returns_none():
    result = _simulate(weekly_amount=50.0, weeks=10)
    assert result["goal_hit_date"] is None
    assert result["projected_total_saved"] == 500.0