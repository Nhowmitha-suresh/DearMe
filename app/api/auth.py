from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.auth import verify_firebase_token, get_current_user
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix='/auth', tags=['auth'])


class TokenExchange(BaseModel):
    id_token: str


@router.post('/firebase', summary='Exchange Firebase ID token for session')
async def firebase_exchange(payload: TokenExchange, db: AsyncSession = Depends(get_db)):
    decoded = await verify_firebase_token(payload.id_token)
    if not decoded:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # ensure user exists
    repo = UserRepository(db)
    user = await repo.get_by_email(decoded.get('email'))
    if not user:
        # create minimal user
        user = await repo.create(User(email=decoded.get('email'), firebase_uid=decoded.get('uid')))

    return {'access_token': payload.id_token, 'token_type': 'bearer', 'user_id': str(user.id)}


@router.get('/me')
async def me(user = Depends(get_current_user)):
    return {'id': str(user.id), 'email': user.email}
