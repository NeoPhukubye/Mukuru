"""Transaction endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session

from ..db import delete_transaction, engine, get_transaction
from ..db import list_transactions as _list
from ..models import (
    Category,
    ErrorResponse,
    Transaction,
    TransactionBulkCreate,
    TransactionCreate,
    TransactionListResponse,
    TransactionUpdate,
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


def _apply_category_rules(
    tx: Transaction, is_remittance: bool | None, category: Category | None
) -> Transaction:
    """Re-resolve the category after an update, honouring the same rules as create."""
    if is_remittance is not None:
        tx.is_remittance = is_remittance
    if tx.is_remittance:
        tx.category = Category.REMITTANCE.value
    elif category is not None:
        tx.category = category.value
    elif tx.category in (None, "", Category.OTHER.value):
        tx.category = build_transaction_category(
            TransactionCreate(
                user_id=tx.user_id,
                date=tx.date,
                amount=tx.amount,
                merchant=tx.merchant,
                description=tx.description,
                type=tx.type,
                category=Category.OTHER,
                is_remittance=tx.is_remittance,
                recipient_country=tx.recipient_country,
            )
        ).value
    return tx


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


@router.get(
    "/{tx_id}",
    response_model=Transaction,
    responses={404: {"model": ErrorResponse}},
)
def get_transaction_detail(
    tx_id: int, user_id: str = Query(..., min_length=1, max_length=64)
) -> Transaction:
    tx = get_transaction(tx_id, user_id)
    if not tx:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "detail": "Transaction not found for this user.",
            },
        )
    return tx


@router.patch(
    "/{tx_id}",
    response_model=Transaction,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
)
def update_transaction_detail(tx_id: int, body: TransactionUpdate) -> Transaction:
    tx = get_transaction(tx_id, body.user_id)
    if not tx:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "detail": "Transaction not found for this user.",
            },
        )

    updates = body.model_dump(exclude_unset=True, exclude_none=True)
    # Never let a client overwrite the ownership column.
    updates.pop("user_id", None)
    if not updates:
        return tx

    for key, value in updates.items():
        if hasattr(value, "value"):
            value = value.value
        setattr(tx, key, value)

    tx = _apply_category_rules(
        tx,
        updates.get("is_remittance"),
        updates.get("category")
        if isinstance(updates.get("category"), Category)
        else None,
    )
    with Session(engine) as session:
        session.add(tx)
        session.commit()
        session.refresh(tx)
    return tx


@router.delete(
    "/{tx_id}",
    responses={404: {"model": ErrorResponse}},
)
def delete_transaction_detail(
    tx_id: int, user_id: str = Query(..., min_length=1, max_length=64)
) -> dict:
    if not delete_transaction(tx_id, user_id):
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "detail": "Transaction not found for this user.",
            },
        )
    return {"deleted": tx_id}