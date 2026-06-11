from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.journal import JournalEntryCreate, JournalEntryRead
from app.services.journal_service import JournalService
from app.schemas.pagination import Page

router = APIRouter(prefix='/journal', tags=['journal'])


@router.post('/', response_model=JournalEntryRead)
async def create_entry(payload: JournalEntryCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = JournalService(db)
    try:
        je = await svc.create_entry(user, payload)
        return JournalEntryRead.from_orm(je)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', response_model=Page[JournalEntryRead])
async def list_entries(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = JournalService(db)
    items, total = await svc.list_entries(user, limit=limit, offset=offset)
    return Page(items=[JournalEntryRead.from_orm(i) for i in items], total=total, limit=limit, offset=offset)
