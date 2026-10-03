"""Simulation endpoint."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from ..db import engine
from ..models import ErrorResponse, Goal, SimulateRequest, SimulateResponse
from ..services.simulator import simulate as _simulate

router = APIRouter(prefix="/simulate", tags=["simulate"])


@router.post("", response_model=SimulateResponse, responses={400: {"model": ErrorResponse}})
def simulate(body: SimulateRequest) -> SimulateResponse:
    goal_target: float | None = None
    goal_saved = 0.0
    if body.goal_id is not None:
        with Session(engine) as session:
            goal = session.get(Goal, body.goal_id)
            if not goal or goal.user_id != body.user_id:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "not_found", "detail": "Goal not found for this user."},
                )
            goal_target = goal.target_amount
            goal_saved = goal.saved_amount

    result = _simulate(
        weekly_amount=body.weekly_amount,
        weeks=body.weeks,
        goal_target=goal_target,
        goal_saved=goal_saved,
    )
    return SimulateResponse(
        user_id=body.user_id,
        weekly_amount=body.weekly_amount,
        weeks=body.weeks,
        projected_balance_by_month=result["projected_balance_by_month"],
        goal_hit_date=result["goal_hit_date"],
        goal_remaining=result["goal_remaining"],
        difference_vs_no_saving=result["difference_vs_no_saving"],
        projected_total_saved=result["projected_total_saved"],
    )