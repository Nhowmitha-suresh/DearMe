from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class IDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )


class AuditMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    updated_by: Mapped[uuid.UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)


class SoftDeleteMixin:
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text('true'), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default=text('false'), nullable=False)


class TimestampMixin(AuditMixin):
    pass


class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'
    prefer_not_to_say = 'prefer_not_to_say'


class ProviderEnum(str, Enum):
    firebase = 'firebase'
    google = 'google'
    email = 'email'
    apple = 'apple'


class MealTypeEnum(str, Enum):
    breakfast = 'breakfast'
    lunch = 'lunch'
    dinner = 'dinner'
    snack = 'snack'


class MoodEnum(str, Enum):
    happy = 'happy'
    calm = 'calm'
    neutral = 'neutral'
    stressed = 'stressed'
    sad = 'sad'
    burned_out = 'burned_out'


class TaskStatusEnum(str, Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    blocked = 'blocked'
    done = 'done'
    archived = 'archived'


class PriorityEnum(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    critical = 'critical'


class EventTypeEnum(str, Enum):
    meeting = 'meeting'
    study = 'study'
    assessment = 'assessment'
    interview = 'interview'
    personal = 'personal'
    health = 'health'


class NotificationStatusEnum(str, Enum):
    pending = 'pending'
    sent = 'sent'
    delivered = 'delivered'
    failed = 'failed'


class GoalStatusEnum(str, Enum):
    not_started = 'not_started'
    in_progress = 'in_progress'
    paused = 'paused'
    completed = 'completed'
    abandoned = 'abandoned'


class PeriodFlowEnum(str, Enum):
    light = 'light'
    medium = 'medium'
    heavy = 'heavy'
    spotting = 'spotting'
    none = 'none'
