from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel, ConfigDict


class AIMemoryCreate(BaseModel):
    memory_type: str
    content: str
    metadata: Optional[dict] = None


class AIMemoryRead(AIMemoryCreate):
    id: uuid.UUID
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    reply: str
    sources: Optional[List[str]] = None
