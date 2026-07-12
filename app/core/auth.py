from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.core.security import decode_access_token
from typing import Optional

security = HTTPBearer()


async def verify_firebase_token(token: str) -> Optional[dict]:
    try:
        import firebase_admin.auth as fb_auth
        decoded = fb_auth.verify_id_token(token)
        return decoded
    except Exception:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    
    # 1. Attempt native JWT decoding
    decoded = decode_access_token(token)
    email = None
    
    if decoded:
        email = decoded.get('email')
    else:
        # 2. Fallback to Firebase validation
        firebase_decoded = await verify_firebase_token(token)
        if firebase_decoded:
            email = firebase_decoded.get('email')
            
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired auth token')

    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user

