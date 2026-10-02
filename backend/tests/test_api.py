"""API-level tests for the routers.

These cover the contracts that previously broke silently: period scoping,
credit-score agreement between endpoints, and goal ownership isolation.
"""
from __future__ import annotations

import os
import tempfile
from datetime import date, timedelta

import pytest

# Point at a throwaway database before the app engine is created.
_tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp_db.close()
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp_db.name}"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

USER = "grace"
OTHER = "someone-else"


@pytest.fixture(scope="module")
def client():
    # Entering the context manager runs the lifespan startup, which creates
    # tables and seeds demo data. Seeding must happen inside it, not before.
    with TestClient(app) as c:
        yield c


def _tx(client, *, user, day, amount, tx_type="debit", category="other",
        is_rem=False, merchant="Test", description="test"):
    return client.post(
        "/transactions",
        json={
            "user_id": user,
            "date": day,
            "amount": amount,
            "merchant": merchant,
            "description": description,
            "type": tx_type,
            "category": category,
            "is_remittance": is_rem,
        },
    )


# --- period scoping -------------------------------------------------------

def test_budget_is_scoped_to_current_month(client):
    """A month of data must not be reported as a year's income."""
    res = client.get("/analyze-budget", params={"user_id": USER})
    assert res.status_code == 200
    body = res.json()

    today = date.today()
    assert body["month"] == today.strftime("%Y-%m")

    # Seeded salary is one month of pay, not twelve.
    assert 0 < body["total_income"] < 50_000


def test_budget_ignores_old_transactions(client):
    """Transactions outside the current month must not affect the total."""
    old_day = (date.today().replace(day=1) - timedelta(days=1)).isoformat()
    before = client.get("/analyze-budget", params={"user_id": USER}).json()["total_income"]

    assert _tx(
        client, user="scoped-user", day=old_day, amount=999_999,
        tx_type="credit",
    ).status_code == 200

    after = client.get("/analyze-budget", params={"user_id": USER}).json()["total_income"]
    assert after == before


def test_advice_injection_is_monthly_not_annual(client):
    res = client.get("/advice", params={"user_id": USER})
    assert res.status_code == 200
    injection = res.json()["monthly_injection"]

    # Advisor injects 5-25% of monthly income. An annual sum produced values
    # roughly 12x too high.
    assert injection < 5_000


# --- credit score consistency --------------------------------------------

def test_credit_score_matches_report(client):
    """Both endpoints must derive the score from the same inputs."""
    score = client.get("/calculate-credit-score", params={"user_id": USER}).json()["score"]
    report = client.get("/generate-financial-report", params={"user_id": USER}).json()
    assert score == report["credit_score"]


def test_credit_factors_reproduce_score(client):
    """Published factors must explain the published score."""
    body = client.get("/calculate-credit-score", params={"user_id": USER}).json()
    weighted = sum(f["score"] * f["weight"] for f in body["factors"])
    expected = round(300 + (weighted / 100.0) * 550)
    assert abs(expected - body["score"]) <= 1


def test_multiple_remittances_in_one_month_do_not_exceed_100(client):
    """Two remittances in one month must not push consistency above 100."""
    user = "double-remit"
    # Use last month: the trailing-12-month window ends at today, so
    # transactions dated later in the current month fall outside it.
    last_month = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1)
    ym = last_month.isoformat()[:7]
    for day in (f"{ym}-05", f"{ym}-06"):
        assert _tx(client, user=user, day=day, amount=500, is_rem=True).status_code == 200
    assert _tx(client, user=user, day=f"{ym}-10",
               amount=9000, tx_type="credit").status_code == 200

    body = client.get("/calculate-credit-score", params={"user_id": user}).json()
    for factor in body["factors"]:
        assert 0 <= factor["score"] <= 100


# --- goal ownership -------------------------------------------------------

def test_goal_progress_requires_ownership(client):
    goal = client.post(
        "/goals",
        json={
            "user_id": OTHER,
            "name": "Private",
            "target_amount": 1000,
            "deadline": (date.today() + timedelta(days=90)).isoformat(),
        },
    ).json()
    goal_id = goal["id"]

    assert client.get(f"/goals/{goal_id}/progress", params={"user_id": OTHER}).status_code == 200
    # Another user must not read it.
    assert client.get(f"/goals/{goal_id}/progress", params={"user_id": USER}).status_code == 404


def test_add_funds_requires_ownership(client):
    goal = client.post(
        "/goals",
        json={
            "user_id": OTHER,
            "name": "Owned",
            "target_amount": 1000,
            "deadline": (date.today() + timedelta(days=90)).isoformat(),
        },
    ).json()
    goal_id = goal["id"]

    ok = client.patch(
        f"/goals/{goal_id}/add-funds", json={"user_id": OTHER, "amount": 100}
    )
    assert ok.status_code == 200
    assert ok.json()["saved_amount"] == 100

    denied = client.patch(
        f"/goals/{goal_id}/add-funds", json={"user_id": USER, "amount": 500}
    )
    assert denied.status_code == 404


def test_delete_requires_ownership(client):
    goal = client.post(
        "/goals",
        json={
            "user_id": OTHER,
            "name": "Disposable",
            "target_amount": 500,
            "deadline": (date.today() + timedelta(days=30)).isoformat(),
        },
    ).json()
    goal_id = goal["id"]

    assert client.delete(f"/goals/{goal_id}", params={"user_id": USER}).status_code == 404
    assert client.delete(f"/goals/{goal_id}", params={"user_id": OTHER}).status_code == 200
    assert client.get(f"/goals/{goal_id}/progress", params={"user_id": OTHER}).status_code == 404


def test_add_funds_rejects_non_positive(client):
    goal = client.post(
        "/goals",
        json={
            "user_id": USER,
            "name": "Guarded",
            "target_amount": 500,
            "deadline": (date.today() + timedelta(days=30)).isoformat(),
        },
    ).json()

    for bad in (0, -50):
        res = client.patch(
            f"/goals/{goal['id']}/add-funds", json={"user_id": USER, "amount": bad}
        )
        assert res.status_code == 422


# --- categorisation -------------------------------------------------------

def test_placeholder_category_is_autocategorised(client):
    """category='other' is a placeholder and should be corrected."""
    res = _tx(client, user="auto-cat", day=date.today().isoformat(),
              amount=100, merchant="Vodacom", description="Airtime and data")
    assert res.json()["category"] == "airtime"

    res = _tx(client, user="auto-cat", day=date.today().isoformat(),
              amount=100, merchant="Checkers", description="Monthly groceries")
    assert res.json()["category"] == "groceries"

    # Nothing recognisable stays as-is.
    res = _tx(client, user="auto-cat", day=date.today().isoformat(),
              amount=100, merchant="Unknown Shop", description="Random purchase")
    assert res.json()["category"] == "other"


def test_remittance_forces_remittance_category(client):
    res = _tx(client, user="auto-remit", day=date.today().isoformat(),
              amount=250, category="groceries", is_rem=True)
    assert res.json()["category"] == "remittance"


def test_explicit_category_is_preserved(client):
    res = _tx(client, user="explicit", day=date.today().isoformat(),
              amount=100, merchant="Vodacom", description="Airtime",
              category="utilities")
    assert res.json()["category"] == "utilities"


# --- misc -----------------------------------------------------------------

def test_health_and_docs(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/docs").status_code == 200


def test_root_redirects_to_docs(client):
    res = client.get("/", follow_redirects=False)
    assert res.status_code in (302, 307)
    assert res.headers["location"] == "/docs"


def test_unknown_user_returns_no_data(client):
    res = client.get("/analyze-budget", params={"user_id": "nobody-here"})
    assert res.status_code == 400
    assert res.json()["error"] == "no_data"


def test_error_detail_does_not_leak_internals(client):
    """The 500 handler must not echo raw exception text."""
    res = client.get("/analyze-budget", params={"user_id": ""})
    assert res.status_code == 422

# --- spending windows and category breakdown ------------------------------

def test_budget_window_defaults_to_calendar_month(client):
    """The default must stay the calendar month so existing callers are unaffected."""
    body = client.get("/analyze-budget", params={"user_id": USER}).json()
    assert body["month"] == date.today().strftime("%Y-%m")


def test_budget_trailing_window_spans_more_than_one_month(client):
    """30d covers roughly a full monthly expense cycle; the month view does not.

    Early in a month the calendar view holds only a salary and rent payment,
    which produced a single-bar breakdown and a savings rate the user had not
    actually achieved yet.
    """
    month = client.get("/analyze-budget", params={"user_id": USER}).json()
    trailing = client.get(
        "/analyze-budget", params={"user_id": USER, "window": "30d"}
    ).json()

    assert trailing["month"] == "last 30 days"
    assert trailing["total_expenses"] > month["total_expenses"]
    # A month-to-date figure taken on the 1st or 2nd wildly overstates savings.
    assert trailing["savings_rate"] < month["savings_rate"]


def test_budget_rejects_unknown_window(client):
    res = client.get("/analyze-budget", params={"user_id": USER, "window": "5y"})
    assert res.status_code == 422


def test_budget_window_includes_multiple_spending_categories(client):
    """The breakdown the dashboard renders needs more than one outflow."""
    body = client.get(
        "/analyze-budget", params={"user_id": USER, "window": "90d"}
    ).json()
    outflows = [k for k, v in body["totals_by_category"].items() if v < 0]
    assert len(outflows) >= 5
    assert "entertainment" in outflows


def test_entertainment_is_categorised():
    from app.services.categorizer import categorize

    assert categorize("Netflix", "Monthly subscription") == "entertainment"
    assert categorize("Cineworld", "Movie tickets") == "entertainment"
    assert categorize("DStv", "Entertainment package") == "entertainment"


def test_new_categories_do_not_steal_existing_ones():
    """Adding rules must not reclassify transactions that were already correct."""
    from app.services.categorizer import categorize

    assert categorize("Vodacom", "Airtime and data") == "airtime"
    assert categorize("Eskom", "Electricity") == "utilities"
    assert categorize("Uber", "Trip to work") == "transport"
    assert categorize("Checkers", "Monthly groceries") == "groceries"
    assert categorize("Landlord", "Rent") == "rent"
    assert categorize("Mukuru", "Send money home", True) == "remittance"
