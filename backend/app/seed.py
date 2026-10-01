"""Seed demo data for user 'Grace'. Idempotent: skips if already present."""
from __future__ import annotations

from datetime import date, datetime, timezone

from sqlmodel import Session, select

from .db import engine
from .models import Goal, Transaction

USER_ID = "grace"
ACCOUNT_HOLDER = "Grace Moyo"


def _d(months_ago: int, day: int = 15) -> date:
    today = date.today()
    y, m = today.year, today.month - months_ago
    while m <= 0:
        m += 12
        y -= 1
    return date(y, m, min(day, 28))


def _build_transactions() -> list[Transaction]:
    txs: list[Transaction] = []
    for i in range(12):
        m = _d(i)
        txs.append(Transaction(
            user_id=USER_ID, date=m, amount=5500.0,
            merchant="Employer", description="Monthly salary", type="credit",
            category="other", is_remittance=False,
        ))
        txs.append(Transaction(
            user_id=USER_ID, date=m.replace(day=1), amount=1800.0,
            merchant="Landlord", description="Rent", type="debit",
            category="rent", is_remittance=False,
        ))
        txs.append(Transaction(
            user_id=USER_ID, date=m.replace(day=3), amount=720.0,
            merchant="Checkers", description="Monthly groceries", type="debit",
            category="groceries", is_remittance=False,
        ))
        txs.append(Transaction(
            user_id=USER_ID, date=m.replace(day=5), amount=180.0,
            merchant="Vodacom", description="Airtime and data", type="debit",
            category="airtime", is_remittance=False,
        ))
        txs.append(Transaction(
            user_id=USER_ID, date=m.replace(day=7), amount=320.0,
            merchant="Taxi", description="Work transport", type="debit",
            category="transport", is_remittance=False,
        ))
        txs.append(Transaction(
            user_id=USER_ID, date=m.replace(day=10), amount=260.0,
            merchant="City Power", description="Electricity", type="debit",
            category="utilities", is_remittance=False,
        ))
        # Remittance — mostly consistent R2 500, sent around day 20.
        # One late month (i == 5 -> 7 days late) to create an on-time pattern.
        remit_day = 20 if i != 5 else 27
        txs.append(Transaction(
            user_id=USER_ID, date=m.replace(day=remit_day), amount=2500.0,
            merchant="Mukuru", description="Send money home", type="debit",
            category="remittance", is_remittance=True, recipient_country="ZW",
        ))
    return txs


def _build_goals() -> list[Goal]:
    today = date.today()
    now = datetime.now(timezone.utc)
    return [
        Goal(
            id=1,
            user_id=USER_ID,
            name="School fees",
            target_amount=12000.0,
            saved_amount=3500.0,
            deadline=date(today.year, 12, 15),
            created_at=now,
        ),
        Goal(
            id=2,
            user_id=USER_ID,
            name="Fridge",
            target_amount=4500.0,
            saved_amount=1200.0,
            deadline=date(today.year, 11, 30),
            created_at=now,
        ),
    ]


def seed() -> None:
    with Session(engine) as session:
        existing = session.exec(
            select(Transaction).where(Transaction.user_id == USER_ID)
        ).first()
        if existing:
            return
        for tx in _build_transactions():
            session.add(tx)
        for g in _build_goals():
            session.add(g)
        session.commit()


if __name__ == "__main__":
    seed()
    print("Seeded demo data for user 'grace'.")