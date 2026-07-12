from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ai_service import AIService
from app.schemas.ai import ChatRequest, ChatResponse, AIMemoryCreate, AIMemoryRead

router = APIRouter(prefix='/ai', tags=['ai'])


@router.post('/chat', response_model=ChatResponse)
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = AIService(db)
    reply, sources = await svc.generate_response(user, req.message)
    return ChatResponse(reply=reply, sources=sources)



@router.post('/memories', response_model=AIMemoryRead)
async def store_memory(payload: AIMemoryCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = AIService(db)
    mem = await svc.store_memory(user, payload.memory_type, payload.content, metadata=payload.metadata)
    return AIMemoryRead.from_orm(mem)
