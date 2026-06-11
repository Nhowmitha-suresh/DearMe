from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import date


class GoalCreate(BaseModel):
    title: str
    description: Optional[str]
    category: Optional[str]


class GoalRead(GoalCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    start_date: Optional[date]
    end_date: Optional[date]

    class Config:
        orm_mode = True
