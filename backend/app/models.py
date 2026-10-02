"""Pydantic + SQLModel models for Money Coach."""
from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from sqlmodel import Field as SQLField, SQLModel


class TransactionType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class Category(str, Enum):
    GROCERIES = "groceries"
    RENT = "rent"
    AIRTIME = "airtime"
    TRANSPORT = "transport"
    REMITTANCE = "remittance"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    HEALTH = "health"
    EDUCATION = "education"
    PERSONAL_CARE = "personal_care"
    FAMILY = "family"
    OTHER = "other"


# --- Persistence model (SQLModel table) ---
class Transaction(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    user_id: str = SQLField(index=True, max_length=64)
    date: date
    amount: float
    merchant: str = SQLField(max_length=128)
    description: str = SQLField(max_length=256)
    type: str
    category: str
    is_remittance: bool = False
    recipient_country: Optional[str] = SQLField(default=None, max_length=8)


class Goal(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    user_id: str = SQLField(index=True, max_length=64)
    name: str = SQLField(max_length=128)
    target_amount: float
    saved_amount: float = 0.0
    deadline: date
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(timezone.utc))


# --- API input contracts (Pydantic) ---
class TransactionCreate(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=64)
    date: date
    amount: float = Field(..., gt=0)
    merchant: str = Field(..., min_length=1, max_length=128)
    description: str = Field(..., min_length=1, max_length=256)
    type: TransactionType
    category: Category
    is_remittance: bool = False
    recipient_country: Optional[str] = Field(default=None, max_length=8)

    @field_validator("recipient_country")
    @classmethod
    def validate_country(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip().upper()
        return v or None


class TransactionBulkCreate(BaseModel):
    transactions: list[TransactionCreate] = Field(..., min_length=1, max_length=200)


class TransactionListResponse(BaseModel):
    items: list[Transaction]
    total: int
    user_id: str


class BudgetAnalysis(BaseModel):
    user_id: str
    month: str
    totals_by_category: dict[str, float]
    total_income: float
    total_expenses: float
    savings_rate: float
    surplus_deficit: float
    insights: list[str]


class GoalCreate(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=64)
    name: str = Field(..., min_length=1, max_length=128)
    target_amount: float = Field(..., gt=0)
    saved_amount: float = Field(default=0, ge=0)
    deadline: date


class GoalFundsUpdate(BaseModel):
    """Body for adding funds to an existing goal."""
    user_id: str = Field(..., min_length=1, max_length=64)
    amount: float = Field(..., gt=0, le=1_000_000)


class GoalProgress(BaseModel):
    id: int
    name: str
    target_amount: float
    saved_amount: float
    percent_complete: float
    amount_remaining: float
    deadline: date
    days_remaining: int
    nudge: str


class SimulateRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=64)
    weekly_amount: float = Field(..., ge=0)
    weeks: int = Field(..., gt=0, le=260)
    goal_id: Optional[int] = None


class SimulateResponse(BaseModel):
    user_id: str
    weekly_amount: float
    weeks: int
    projected_balance_by_month: list[dict]
    goal_hit_date: Optional[str] = None
    goal_remaining: Optional[float] = None
    difference_vs_no_saving: float
    projected_total_saved: float


class AdviceResponse(BaseModel):
    user_id: str
    monthly_injection: float
    allocation: dict[str, float]
    rationale: str
    pools: list[dict]


class CreditFactor(BaseModel):
    name: str
    weight: float
    score: int
    detail: str


class CreditScoreResponse(BaseModel):
    user_id: str
    score: int
    band: str
    factors: list[CreditFactor]
    tips: list[str]
    history: list[dict]


class ReportResponse(BaseModel):
    user_id: str
    account_holder: str
    generated_at: datetime
    period_months: int
    income_summary: dict
    category_breakdown: list[dict]
    credit_score: int
    disclaimer: str


class CoachChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=64)
    message: str = Field(..., min_length=1, max_length=1024)


class CoachChatResponse(BaseModel):
    reply: str
    suggested_actions: list[str]


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


class FxConversion(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float
    rate: Optional[float] = None
    symbol: str
    converted: bool


class FxCurrencies(BaseModel):
    currencies: list[dict]