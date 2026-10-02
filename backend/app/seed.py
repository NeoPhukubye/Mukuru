"""Seed demo data for user 'Grace'. Idempotent: skips if already present."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlmodel import Session, select

from .config import DEMO_ACCOUNT_HOLDER, DEMO_USER_ID
from .db import engine
from .models import Goal, Transaction

USER_ID = DEMO_USER_ID
ACCOUNT_HOLDER = DEMO_ACCOUNT_HOLDER

# (day, amount, merchant, description, type, category, is_remittance)
_MONTHLY = [
    (1, 8000.0, "Employer", "Monthly salary", "credit", "other", False),
    (1, 1800.0, "Landlord", "Rent", "debit", "rent", False),
    (2, 250.0, "Little Steps Creche", "Creche monthly fee", "debit", "education", False),
    (3, 720.0, "Checkers", "Monthly groceries", "debit", "groceries", False),
    (4, 180.0, "Clicks Pharmacy", "Monthly medication", "debit", "health", False),
    (5, 180.0, "Vodacom", "Airtime and data", "debit", "airtime", False),
    (6, 300.0, "DStv", "Entertainment package", "debit", "entertainment", False),
    (7, 320.0, "Taxi", "Work transport", "debit", "transport", False),
    (8, 120.0, "Ubuntu Hair Salon", "Haircut", "debit", "personal_care", False),
    (9, 150.0, "Baby City", "Nappies and baby items", "debit", "family", False),
    (10, 260.0, "City Power", "Electricity", "debit", "utilities", False),
    (20, 2500.0, "Mukuru", "Send money home", "debit", "remittance", True),
]


def _month_start(months_ago: int, today: date) -> date:
    y, m = today.year, today.month - months_ago
    while m <= 0:
        m += 12
        y -= 1
    return date(y, m, 1)


def _build_transactions() -> list[Transaction]:
    """12 months of history, never dated after today.

    The previous seed dated every month on fixed days without checking the
    calendar, so on the 2nd of the month it created transactions dated later
    that month — including a salary that had not been paid yet. Those rows
    then made the budget and report claim money that did not exist yet.
    """
    today = date.today()
    txs: list[Transaction] = []
    for i in range(12):
        first = _month_start(i, today)
        for day, amount, merchant, desc, typ, cat, is_rem in _MONTHLY:
            # One late remittance (month 5) so the on-time factor is not perfect.
            if is_rem and i == 5:
                day = 27
            d = first.replace(day=day)
            if d > today:
                continue
            txs.append(Transaction(
                user_id=USER_ID, date=d, amount=amount, merchant=merchant,
                description=desc, type=typ, category=cat, is_remittance=is_rem,
                recipient_country="ZW" if is_rem else None,
            ))
    return txs


def _build_goals() -> list[Goal]:
    """Deadlines are relative to today so the demo never opens on an expired goal."""
    today = date.today()
    now = datetime.now(timezone.utc)
    return [
        Goal(
            user_id=USER_ID, name="School fees", target_amount=12000.0,
            saved_amount=3500.0, deadline=today + timedelta(days=75),
            created_at=now,
        ),
        Goal(
            user_id=USER_ID, name="Fridge", target_amount=4500.0,
            saved_amount=1200.0, deadline=today + timedelta(days=60),
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