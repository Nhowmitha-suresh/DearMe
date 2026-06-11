from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from typing import Optional

security = HTTPBearer()


async def verify_firebase_token(token: str) -> Optional[dict]:
    # Placeholder: integrate firebase_admin.auth.verify_id_token
    # Return dict with 'uid' if valid, else raise
    try:
        # import firebase_admin and verify
        import firebase_admin.auth as fb_auth
        decoded = fb_auth.verify_id_token(token)
        return decoded
    except Exception:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    decoded = await verify_firebase_token(token)
    if not decoded:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid auth token')

    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(decoded.get('email'))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user
