"""SQLite persistence via SQLModel."""
from __future__ import annotations

import os
from typing import Optional

from sqlmodel import SQLModel, Session, create_engine, select

from .models import Transaction, Goal

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
    with Session(engine) as session:
        return session.get(Goal, goal_id)


def delete_goal(goal_id: int, user_id: str) -> bool:
    with Session(engine) as session:
        goal = session.get(Goal, goal_id)
        if not goal or goal.user_id != user_id:
            return False
        session.delete(goal)
        session.commit()
        return True