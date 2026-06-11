from fastapi import APIRouter

from .ai import router as ai_router
from .auth import router as auth_router
from .goals import router as goals_router
from .health import router as health_router
from .journal import router as journal_router
from .notifications import router as notifications_router
from .tasks import router as tasks_router
from .users import router as users_router


api_router = APIRouter(prefix='/api/v1')
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(health_router)
api_router.include_router(goals_router)
api_router.include_router(tasks_router)
api_router.include_router(journal_router)
api_router.include_router(notifications_router)
api_router.include_router(ai_router)