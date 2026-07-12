import uuid
from datetime import date, datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict


class ExpenseBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    logged_at: Optional[datetime] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseRead(ExpenseBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SavingsGoalBase(BaseModel):
    title: str
    target_amount: float
    current_amount: Optional[float] = 0.00
    target_date: Optional[date] = None


class SavingsGoalCreate(SavingsGoalBase):
    pass


class SavingsGoalRead(SavingsGoalBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class CategorySpend(BaseModel):
    category: str
    total: float


class FinanceSummary(BaseModel):
    total_expenses: float
    category_breakdown: List[CategorySpend]
    savings_progress: List[SavingsGoalRead]
