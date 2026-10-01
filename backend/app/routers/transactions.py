"""Transaction endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session

from ..db import engine, list_transactions as _list
from ..models import (
    Category,
    ErrorResponse,
    Transaction,
    TransactionBulkCreate,
    TransactionCreate,
    TransactionListResponse,
)
from ..services.categorizer import build_transaction_category

router = APIRouter(prefix="/transactions", tags=["transactions"])


def _to_model(tx: TransactionCreate) -> Transaction:
    """Build the persistence model.

    The client may send category="other" as a placeholder, in which case the
    rule-based categoriser fills it in. Previously the guard read
    `if not tx.category`, which was never true because the field is required,
    so auto-categorisation never ran.
    """
    data = tx.model_dump()
    if tx.is_remittance:
        data["category"] = Category.REMITTANCE.value
    elif data.get("category") in (None, "", Category.OTHER.value):
        data["category"] = build_transaction_category(tx).value
    data["type"] = tx.type.value
    return Transaction(**data)


@router.post("", response_model=Transaction, responses={400: {"model": ErrorResponse}})
def create_transaction(tx: TransactionCreate) -> Transaction:
    obj = _to_model(tx)
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        session.refresh(obj)
    return obj


@router.post("/bulk", response_model=list[Transaction], responses={400: {"model": ErrorResponse}})
def create_transactions_bulk(body: TransactionBulkCreate) -> list[Transaction]:
    objs: list[Transaction] = []
    with Session(engine) as session:
        for tx in body.transactions:
            obj = _to_model(tx)
            session.add(obj)
            objs.append(obj)
        session.commit()
        for o in objs:
            session.refresh(o)
    return objs


@router.get("", response_model=TransactionListResponse)
def list_transactions(
    user_id: str = Query(..., min_length=1, max_length=64),
    category: str | None = Query(default=None),
    from_: str | None = Query(default=None, alias="from"),
    to: str | None = Query(default=None),
) -> TransactionListResponse:
    items = _list(user_id, category, from_, to)
    return TransactionListResponse(items=items, total=len(items), user_id=user_id)