import uuid
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CodingProfileBase(BaseModel):
    leetcode_username: Optional[str] = None
    github_username: Optional[str] = None
    is_active: Optional[bool] = True


class CodingProfileCreate(CodingProfileBase):
    pass


class CodingProfileRead(CodingProfileBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class CodingActivityBase(BaseModel):
    commits_count: Optional[int] = 0
    problems_solved: Optional[int] = 0
    logged_date: Optional[date] = None


class CodingActivityCreate(CodingActivityBase):
    pass


class CodingActivityRead(CodingActivityBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
