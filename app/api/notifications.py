from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user
from app.services.notification_service import NotificationService
from app.schemas.pagination import Page

router = APIRouter(prefix='/notifications', tags=['notifications'])


@router.get('/', response_model=Page)
async def list_notifications(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = NotificationService(db)
    items, total = await svc.list_notifications(user, limit=limit, offset=offset)
    return Page(items=[{'id': str(i.id), 'message': i.message, 'scheduled_at': i.scheduled_at, 'status': i.status} for i in items], total=total, limit=limit, offset=offset)


@router.post('/{notification_id}/mark_read')
async def mark_read(notification_id: str, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    svc = NotificationService(db)
    n = await svc.mark_read(notification_id, user)
    if not n:
        raise HTTPException(status_code=404, detail='notification not found')
    return {'status': 'ok'}
