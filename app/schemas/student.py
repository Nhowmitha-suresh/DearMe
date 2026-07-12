import uuid
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class SubjectBase(BaseModel):
    name: str
    code: Optional[str] = None
    credits: Optional[float] = None


class SubjectCreate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class LearningSessionBase(BaseModel):
    subject_id: uuid.UUID
    start_time: datetime
    end_time: datetime
    focus_duration_minutes: int
    quality_score: Optional[int] = None
    notes: Optional[str] = None


class LearningSessionCreate(LearningSessionBase):
    pass


class LearningSessionRead(LearningSessionBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class CalendarEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: Optional[str] = None  # e.g., 'class', 'exam', 'personal'
    start_at: datetime
    end_at: datetime
    location: Optional[str] = None
    recurring_rule: Optional[str] = None


class CalendarEventCreate(CalendarEventBase):
    pass


class CalendarEventRead(CalendarEventBase):
    id: uuid.UUID
    owner_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
