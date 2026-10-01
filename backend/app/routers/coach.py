"""Coach chat endpoint."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from ..db import engine
from ..models import CoachChatRequest, CoachChatResponse, ErrorResponse, Transaction
from ..services.coach import chat as _chat

router = APIRouter(prefix="/coach", tags=["coach"])


@router.post("/chat", response_model=CoachChatResponse, responses={400: {"model": ErrorResponse}})
def coach_chat(body: CoachChatRequest) -> CoachChatResponse:
    with Session(engine) as session:
        has_data = session.exec(
            select(Transaction).where(Transaction.user_id == body.user_id)
        ).first()
    if not has_data:
        raise HTTPException(
            status_code=400,
            detail={"error": "no_data", "detail": "No transactions found for this user."},
        )
    return _chat(body.user_id, body.message)