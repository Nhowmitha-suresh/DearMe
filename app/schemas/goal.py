from __future__ import annotations

from datetime import date
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict


class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None


class GoalRead(GoalCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)
