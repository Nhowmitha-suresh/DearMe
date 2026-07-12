from __future__ import annotations

from datetime import datetime, date
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict


class WaterLogCreate(BaseModel):
    amount_ml: int
    logged_at: Optional[datetime] = None


class WaterLogRead(WaterLogCreate):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class SleepLogCreate(BaseModel):
    sleep_time: datetime
    wake_time: datetime


class MealLogCreate(BaseModel):
    meal_type: str
    eaten_at: datetime
    calories: Optional[int] = None


class PeriodCycleCreate(BaseModel):
    start_date: date
    end_date: Optional[date] = None


class PeriodCycleRead(PeriodCycleCreate):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class PeriodSymptomCreate(BaseModel):
    cycle_id: uuid.UUID
    symptom: str
    severity: int


class PeriodPredictionRead(BaseModel):
    predicted_start: date
    predicted_end: date
    ovulation_date: date
    confidence: float

