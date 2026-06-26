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
    # Example flow: store short-term memory and echo; real integration calls Gemini + RAG
    conv = await svc.start_conversation(user, topic=req.context.get('topic') if req.context else None)
    msg = await svc.add_message(conv, 'user', req.message)
    # echo reply for now
    reply = f"Echo: {req.message}"
    await svc.add_message(conv, 'assistant', reply)
    return ChatResponse(reply=reply, sources=[])


@router.post('/memories', response_model=AIMemoryRead)
async def store_memory(payload: AIMemoryCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = AIService(db)
    mem = await svc.store_memory(user, payload.memory_type, payload.content, metadata=payload.metadata)
    return AIMemoryRead.from_orm(mem)
