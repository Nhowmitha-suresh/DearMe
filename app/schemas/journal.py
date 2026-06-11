from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime


class JournalEntryCreate(BaseModel):
    title: Optional[str]
    content: str
    mood: Optional[str]
    tags: Optional[List[str]]


class JournalEntryRead(JournalEntryCreate):
    id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True
