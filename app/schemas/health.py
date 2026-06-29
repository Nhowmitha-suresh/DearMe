from __future__ import annotations

from datetime import datetime
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
