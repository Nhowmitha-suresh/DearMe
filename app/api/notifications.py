from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.notifications import Notification

router = APIRouter(prefix='/notifications', tags=['notifications'])


@router.get('/', response_model=list)
async def list_notifications(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    q = await db.execute('SELECT * FROM notifications WHERE user_id = :uid ORDER BY scheduled_at DESC LIMIT 100', {'uid': str(user.id)})
    return []


@router.post('/{notification_id}/mark_read')
async def mark_read(notification_id: str, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    await db.execute('UPDATE notifications SET read_at = now() WHERE id = :nid AND user_id = :uid', {'nid': notification_id, 'uid': str(user.id)})
    await db.commit()
    return {'status': 'ok'}
