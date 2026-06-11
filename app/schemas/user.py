from __future__ import annotations
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import date


class UserBase(BaseModel):
    email: EmailStr
    primary_phone: Optional[str]


class UserCreate(UserBase):
    firebase_uid: Optional[str]


class UserRead(UserBase):
    id: uuid.UUID
    created_at: Optional[date]

    class Config:
        orm_mode = True


class UserProfileCreate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]


class UserProfileRead(UserProfileCreate):
    id: uuid.UUID
    class Config:
        orm_mode = True
