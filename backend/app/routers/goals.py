"""Goals endpoints."""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from ..db import add_goal, add_goal_funds, delete_goal, get_goal, list_goals
from ..models import ErrorResponse, Goal, GoalCreate, GoalFundsUpdate, GoalProgress

router = APIRouter(prefix="/goals", tags=["goals"])


def _progress(goal: Goal) -> GoalProgress:
    pct = (
        round(min(100.0, (goal.saved_amount / goal.target_amount) * 100.0), 1)
        if goal.target_amount
        else 0.0
    )
    remaining = round(max(0.0, goal.target_amount - goal.saved_amount), 2)
    days_left = max(0, (goal.deadline - date.today()).days)
    if pct >= 100:
        nudge = "Goal complete — you did it! Consider setting a new target."
    elif days_left <= 0:
        nudge = (
            f"Deadline passed for '{goal.name}'. R{remaining:,.0f} still to go "
            "— let's make a plan."
        )
    elif remaining < 500:
        nudge = (
            f"You're only R{remaining:,.0f} away from your {goal.name} goal "
            "— almost there!"
        )
    else:
        daily = remaining / max(1, days_left)
        nudge = (
            f"You're {pct:.0f}% toward your {goal.name} goal. Save about "
            f"R{daily:,.0f}/day to hit it on time."
        )
    return GoalProgress(
        id=goal.id,
        name=goal.name,
        target_amount=goal.target_amount,
        saved_amount=goal.saved_amount,
        percent_complete=pct,
        amount_remaining=remaining,
        deadline=goal.deadline,
        days_remaining=days_left,
        nudge=nudge,
    )


@router.post("", response_model=Goal, responses={400: {"model": ErrorResponse}})
def create_goal(body: GoalCreate) -> Goal:
    return add_goal(Goal(**body.model_dump()))


@router.get("", response_model=list[Goal])
def get_goals(user_id: str = Query(..., min_length=1, max_length=64)) -> list[Goal]:
    return list_goals(user_id)


@router.get(
    "/{goal_id}/progress",
    response_model=GoalProgress,
    responses={404: {"model": ErrorResponse}},
)
def goal_progress(
    goal_id: int, user_id: str = Query(..., min_length=1, max_length=64)
) -> GoalProgress:
    goal = get_goal(goal_id, user_id)
    if not goal:
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "detail": "Goal not found."},
        )
    return _progress(goal)


@router.delete("/{goal_id}", responses={404: {"model": ErrorResponse}})
def remove_goal(goal_id: int, user_id: str = Query(..., min_length=1, max_length=64)) -> dict:
    """Delete a goal. Scoped to the owner, so one user cannot delete another's."""
    if not delete_goal(goal_id, user_id):
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "detail": "Goal not found."},
        )
    return {"deleted": goal_id}


@router.patch(
    "/{goal_id}/add-funds",
    response_model=GoalProgress,
    responses={404: {"model": ErrorResponse}},
)
def add_funds(goal_id: int, body: GoalFundsUpdate) -> GoalProgress:
    """Add money to a goal and return its updated progress."""
    goal = add_goal_funds(goal_id, body.user_id, body.amount)
    if not goal:
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "detail": "Goal not found."},
        )
    return _progress(goal)