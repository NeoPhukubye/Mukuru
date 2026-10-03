"""Unit tests for pure service functions."""
from __future__ import annotations

from datetime import date

from app.models import TransactionCreate
from app.services.categorizer import build_transaction_category, categorize, category_totals
from app.services.credit_engine import compute_credit_score
from app.services.simulator import simulate as _simulate


def test_categorize_remittance() -> None:
    tx = TransactionCreate(
        user_id="u", date=date.today(), amount=2500.0,
        merchant="Mukuru", description="Send money home", type="debit",
        category="other", is_remittance=True, recipient_country="ZW",
    )
    assert build_transaction_category(tx).value == "remittance"


def test_categorize_groceries() -> None:
    assert categorize("Checkers", "Monthly groceries").value == "groceries"
    assert categorize("Shoprite", "Food shopping").value == "groceries"


def test_categorize_rent() -> None:
    assert categorize("Landlord", "Rent payment").value == "rent"


def test_categorize_airtime() -> None:
    assert categorize("Vodacom", "Airtime and data").value == "airtime"


def test_categorize_transport() -> None:
    assert categorize("Taxi", "Work transport").value == "transport"


def test_categorize_utilities() -> None:
    assert categorize("City Power", "Electricity bill").value == "utilities"


def test_categorize_other() -> None:
    assert categorize("Unknown Shop", "Random purchase").value == "other"


def test_category_totals_debits_credits() -> None:
    txs = [
        TransactionCreate(
            user_id="u", date=date.today(), amount=1000.0,
            merchant="A", description="x", type="credit", category="other",
            is_remittance=False,
        ),
        TransactionCreate(
            user_id="u", date=date.today(), amount=300.0,
            merchant="B", description="y", type="debit", category="groceries",
            is_remittance=False,
        ),
    ]
    totals = category_totals(txs)
    assert totals["other"] == 1000.0
    assert totals["groceries"] == -300.0


def test_credit_score_range() -> None:
    score, band, factors, tips = compute_credit_score(
        user_id="grace",
        remittance_months=11,
        total_months=12,
        remittance_amounts=[2500.0] * 11,
        late_months=1,
        tenure_months=12,
        savings_rate=0.12,
    )
    assert 300 <= score <= 850
    assert band in {"Poor", "Fair", "Good", "Very Good", "Excellent"}
    assert len(factors) == 5
    assert sum(f.weight for f in factors) == 1.0
    assert len(tips) >= 1


def test_credit_score_perfect() -> None:
    score, band, _, _ = compute_credit_score(
        user_id="grace",
        remittance_months=12,
        total_months=12,
        remittance_amounts=[2500.0] * 12,
        late_months=0,
        tenure_months=12,
        savings_rate=0.25,
    )
    assert score >= 750
    assert band == "Excellent"


def test_simulate_basic() -> None:
    result = _simulate(weekly_amount=100.0, weeks=52, goal_target=5200.0, goal_saved=0.0)
    assert result["projected_total_saved"] >= 5000.0
    assert result["goal_hit_date"] is not None
    assert result["difference_vs_no_saving"] > 0


def test_simulate_no_goal() -> None:
    result = _simulate(weekly_amount=50.0, weeks=10)
    assert result["goal_hit_date"] is None
    assert result["projected_total_saved"] == 500.0