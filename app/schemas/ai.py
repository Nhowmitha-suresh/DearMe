from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime


class AIMemoryCreate(BaseModel):
    memory_type: str
    content: str
    metadata: Optional[dict] = None


class AIMemoryRead(AIMemoryCreate):
    id: uuid.UUID
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    reply: str
    sources: Optional[List[str]] = None
