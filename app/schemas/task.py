from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str]


class TaskRead(TaskCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    due_date: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True
