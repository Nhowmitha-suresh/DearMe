from __future__ import annotations

from datetime import date
from typing import Optional
import uuid

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    primary_phone: Optional[str] = None


class UserCreate(UserBase):
    firebase_uid: Optional[str] = None


class UserRead(UserBase):
    id: uuid.UUID
    created_at: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class UserProfileCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None


class UserProfileRead(UserProfileCreate):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
