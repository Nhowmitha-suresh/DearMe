from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.services.river_service import RiverService

router = APIRouter(prefix='/river', tags=['river'])


@router.get('/state')
async def get_river_state(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    svc = RiverService(db)
    try:
        state = await svc.get_river_state(user.id)
        return state
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate river state: {str(e)}")
