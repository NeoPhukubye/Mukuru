"""SQLite persistence via SQLModel."""
from __future__ import annotations

import os
from datetime import date, timedelta
from typing import Any, Optional

from sqlmodel import Session, SQLModel, create_engine, select

from .models import Goal, Transaction

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./moneycoach.db")

connect_args: dict = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)


def add_transaction(tx: Transaction) -> Transaction:
    with Session(engine) as session:
        session.add(tx)
        session.commit()
        session.refresh(tx)
        return tx


def add_transactions_bulk(txs: list[Transaction]) -> list[Transaction]:
    if not txs:
        return []
    with Session(engine) as session:
        for tx in txs:
            session.add(tx)
        session.commit()
        for tx in txs:
            session.refresh(tx)
        return txs


def list_transactions(
    user_id: str,
    category: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> list[Transaction]:
    with Session(engine) as session:
        stmt = select(Transaction).where(Transaction.user_id == user_id)
        if category:
            stmt = stmt.where(Transaction.category == category)
        if from_date:
            stmt = stmt.where(Transaction.date >= from_date)
        if to_date:
            stmt = stmt.where(Transaction.date <= to_date)
        stmt = stmt.order_by(Transaction.date)
        return list(session.exec(stmt).all())


def get_transaction(tx_id: int, user_id: str) -> Optional[Transaction]:
    """Return the transaction only if it belongs to user_id, else None."""
    with Session(engine) as session:
        tx = session.get(Transaction, tx_id)
        if not tx or tx.user_id != user_id:
            return None
        return tx


def update_transaction(
    tx_id: int, user_id: str, fields: dict[str, Any]
) -> Optional[Transaction]:
    """Apply a partial update to an owned transaction. None if not found."""
    if not fields:
        return get_transaction(tx_id, user_id)
    with Session(engine) as session:
        tx = session.get(Transaction, tx_id)
        if not tx or tx.user_id != user_id:
            return None
        for key, value in fields.items():
            setattr(tx, key, value)
        session.add(tx)
        session.commit()
        session.refresh(tx)
        return tx


def delete_transaction(tx_id: int, user_id: str) -> bool:
    """Delete a transaction. Scoped to the owner, so one user cannot delete another's."""
    with Session(engine) as session:
        tx = session.get(Transaction, tx_id)
        if not tx or tx.user_id != user_id:
            return False
        session.delete(tx)
        session.commit()
        return True


def add_goal(goal: Goal) -> Goal:
    with Session(engine) as session:
        session.add(goal)
        session.commit()
        session.refresh(goal)
        return goal


def list_goals(user_id: str) -> list[Goal]:
    with Session(engine) as session:
        stmt = select(Goal).where(Goal.user_id == user_id).order_by(Goal.deadline)
        return list(session.exec(stmt).all())


def get_goal(goal_id: int, user_id: str) -> Optional[Goal]:
    """Return the goal only if it belongs to user_id, else None."""
    with Session(engine) as session:
        goal = session.get(Goal, goal_id)
        if not goal or goal.user_id != user_id:
            return None
        return goal


# --- Period helpers -------------------------------------------------------
# Aggregations used to sum every transaction ever and label the result as a
# single month, which inflated monthly figures by the length of the history.
# These helpers give every router the same explicit window.

def current_month_range(today: Optional[date] = None) -> tuple[date, date]:
    """Return (first_day, last_day) of the month containing `today`."""
    ref = today or date.today()
    first = ref.replace(day=1)
    if ref.month == 12:
        last = ref.replace(year=ref.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last = ref.replace(month=ref.month + 1, day=1) - timedelta(days=1)
    return first, last


def trailing_months_range(months: int, today: Optional[date] = None) -> tuple[date, date]:
    """Return (first_day, today) covering the trailing `months` months."""
    ref = today or date.today()
    first, _ = current_month_range(ref)
    start = first
    for _ in range(max(0, months - 1)):
        start = (start - timedelta(days=1)).replace(day=1)
    return start, ref


def list_transactions_for_period(
    user_id: str,
    from_date: date,
    to_date: date,
) -> list[Transaction]:
    """Transactions for a user within an inclusive date window."""
    with Session(engine) as session:
        stmt = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .where(Transaction.date >= from_date)
            .where(Transaction.date <= to_date)
            .order_by(Transaction.date)
        )
        return list(session.exec(stmt).all())


def delete_goal(goal_id: int, user_id: str) -> bool:
    with Session(engine) as session:
        goal = session.get(Goal, goal_id)
        if not goal or goal.user_id != user_id:
            return False
        session.delete(goal)
        session.commit()
        return True


def add_goal_funds(goal_id: int, user_id: str, amount: float) -> Optional[Goal]:
    """Increment a goal's saved_amount, enforcing ownership. None if not found."""
    if amount <= 0:
        return None
    with Session(engine) as session:
        goal = session.get(Goal, goal_id)
        if not goal or goal.user_id != user_id:
            return None
        goal.saved_amount = round(goal.saved_amount + amount, 2)
        session.add(goal)
        session.commit()
        session.refresh(goal)
        return goal