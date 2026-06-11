from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.journal import JournalEntryCreate, JournalEntryRead
from app.models.journal import JournalEntry

router = APIRouter(prefix='/journal', tags=['journal'])


@router.post('/', response_model=JournalEntryRead)
async def create_entry(payload: JournalEntryCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    entry = JournalEntry(user_id=user.id, title=payload.title, content=payload.content, mood=payload.mood)
    db.add(entry)
    await db.flush()
    return JournalEntryRead.from_orm(entry)


@router.get('/', response_model=list[JournalEntryRead])
async def list_entries(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    q = await db.execute('SELECT * FROM journal_entries WHERE user_id = :uid ORDER BY created_at DESC LIMIT 50', {'uid': str(user.id)})
    return []
