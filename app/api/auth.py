from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.auth import verify_firebase_token, get_current_user
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserRegister, UserLogin, ForgotPasswordRequest

router = APIRouter(prefix='/auth', tags=['auth'])


class TokenExchange(BaseModel):
    id_token: str


@router.post('/firebase', summary='Exchange Firebase ID token for session')
async def firebase_exchange(payload: TokenExchange, db: AsyncSession = Depends(get_db)):
    decoded = await verify_firebase_token(payload.id_token)
    if not decoded:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    email = decoded.get('email')
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Firebase token is missing email')

    repo = UserRepository(db)
    user = await repo.get_by_email(email)
    if not user:
        user = await repo.create(User(email=email, firebase_uid=decoded.get('uid')))

    return {'access_token': payload.id_token, 'token_type': 'bearer', 'user_id': str(user.id)}


@router.post('/signup', summary='Register new email & password account')
async def signup(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    existing_user = await repo.get_by_email(payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='An account with this email already exists'
        )
    
    hashed = hash_password(payload.password)
    user = User(
        email=payload.email,
        password_hash=hashed,
        primary_phone=payload.primary_phone
    )
    new_user = await repo.create(user)
    await db.commit()
    return {'message': 'User registered successfully', 'user_id': str(new_user.id)}


@router.post('/login', summary='Log in with email & password')
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_email(payload.email)
    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )
        
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )
        
    # Generate native JWT access token
    access_token = create_access_token({'sub': str(user.id), 'email': user.email})
    return {'access_token': access_token, 'token_type': 'bearer', 'user_id': str(user.id)}


@router.post('/forgot-password', summary='Request password reset link')
async def forgot_password(payload: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_email(payload.email)
    # Return 200 regardless of user existence for privacy security
    return {'message': 'If the email exists, a password reset link has been sent'}


@router.get('/me')
async def me(user = Depends(get_current_user)):
    return {'id': str(user.id), 'email': user.email}

