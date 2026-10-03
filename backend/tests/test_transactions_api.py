"""Tests for the transaction detail/update/delete endpoints.

These endpoints did not exist before: the API only supported creating and
listing transactions, so the dashboard could never correct a typo or remove a
mistake. Ownership isolation is enforced the same way as goals.
"""
from __future__ import annotations

import os
import tempfile
from datetime import date

import pytest

# Point at a throwaway database before the app engine is created, exactly like
# test_api.py. Doing it here too keeps this module importable on its own.
_tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp_db.close()
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp_db.name}"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

USER = "grace"


@pytest.fixture(scope="module")
def client():
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


def _create(client, *, user=USER, day=None, amount=100, merchant="Test",
            description="test", tx_type="debit", category="other",
            is_rem=False):
    day = day or date.today().isoformat()
    return _tx(client, user=user, day=day, amount=amount, tx_type=tx_type,
               category=category, is_rem=is_rem, merchant=merchant,
               description=description)


def test_get_transaction_detail(client):
    res = _create(client, merchant="Vodacom", description="Airtime")
    tx_id = res.json()["id"]

    got = client.get(f"/transactions/{tx_id}", params={"user_id": USER})
    assert got.status_code == 200
    assert got.json()["id"] == tx_id
    assert got.json()["category"] == "airtime"


def test_get_transaction_detail_requires_ownership(client):
    res = _create(client, user="owner-x", merchant="Landlord", description="Rent")
    tx_id = res.json()["id"]

    assert client.get(f"/transactions/{tx_id}", params={"user_id": USER}).status_code == 404
    assert client.get(f"/transactions/{tx_id}", params={"user_id": "owner-x"}).status_code == 200


def test_update_transaction(client):
    res = _create(client, merchant="Unknown Shop", description="Random purchase")
    tx_id = res.json()["id"]

    patched = client.patch(
        f"/transactions/{tx_id}",
        json={"user_id": USER, "merchant": "Checkers", "description": "Monthly groceries"},
    )
    assert patched.status_code == 200
    assert patched.json()["category"] == "groceries"
    assert patched.json()["merchant"] == "Checkers"


def test_update_remittance_forces_category(client):
    # category="other" is a placeholder, so the matcher runs on create.
    res = _create(client, category="other", merchant="Checkers",
                  description="Monthly groceries")
    tx_id = res.json()["id"]
    assert res.json()["category"] == "groceries"

    patched = client.patch(
        f"/transactions/{tx_id}",
        json={"user_id": USER, "is_remittance": True},
    )
    assert patched.status_code == 200
    assert patched.json()["category"] == "remittance"
    assert patched.json()["is_remittance"] is True


def test_update_amount_rejects_non_positive(client):
    res = _create(client)
    tx_id = res.json()["id"]

    bad = client.patch(
        f"/transactions/{tx_id}",
        json={"user_id": USER, "amount": 0},
    )
    assert bad.status_code == 422

    neg = client.patch(
        f"/transactions/{tx_id}",
        json={"user_id": USER, "amount": -50},
    )
    assert neg.status_code == 422


def test_update_requires_ownership(client):
    res = _create(client, user="owner-y")
    tx_id = res.json()["id"]

    denied = client.patch(
        f"/transactions/{tx_id}",
        json={"user_id": USER, "merchant": "hacked"},
    )
    assert denied.status_code == 404


def test_update_unknown_id_is_not_found(client):
    res = client.patch(
        "/transactions/99999",
        json={"user_id": USER, "merchant": "x"},
    )
    assert res.status_code == 404


def test_delete_transaction(client):
    res = _create(client)
    tx_id = res.json()["id"]

    deleted = client.delete(f"/transactions/{tx_id}", params={"user_id": USER})
    assert deleted.status_code == 200
    assert deleted.json()["deleted"] == tx_id

    assert client.get(f"/transactions/{tx_id}", params={"user_id": USER}).status_code == 404


def test_delete_requires_ownership(client):
    res = _create(client, user="owner-z")
    tx_id = res.json()["id"]

    assert client.delete(f"/transactions/{tx_id}", params={"user_id": USER}).status_code == 404
    assert client.delete(f"/transactions/{tx_id}", params={"user_id": "owner-z"}).status_code == 200


def test_update_my_transaction_does_not_change_other_users_budget(client):
    """Editing one user's data must not shift another's budget totals."""
    other = "budget-isolation"
    _create(client, user=other, amount=500, tx_type="credit")
    before = client.get("/analyze-budget", params={"user_id": other}).json()["total_income"]

    mine = _create(client, merchant="Checkers", description="Monthly groceries")
    client.patch(
        f"/transactions/{mine.json()['id']}",
        json={"user_id": USER, "amount": 999_999},
    )

    after = client.get("/analyze-budget", params={"user_id": other}).json()["total_income"]
    assert after == before