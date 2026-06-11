from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class WaterLogCreate(BaseModel):
    amount_ml: int
    logged_at: Optional[datetime]


class WaterLogRead(WaterLogCreate):
    id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        orm_mode = True


class SleepLogCreate(BaseModel):
    sleep_time: datetime
    wake_time: datetime


class MealLogCreate(BaseModel):
    meal_type: str
    eaten_at: datetime
    calories: Optional[int]
