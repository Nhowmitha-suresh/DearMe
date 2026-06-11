from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/ai', tags=['ai'])


class ChatRequest(BaseModel):
    message: str
    context: dict | None = None


class ChatResponse(BaseModel):
    reply: str
    sources: list | None = None


@router.post('/chat', response_model=ChatResponse)
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # Placeholder for AI service integration (Gemini + ChromaDB)
    # For now echo
    return ChatResponse(reply=f"Echo: {req.message}")
