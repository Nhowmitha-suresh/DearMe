from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, Text, DateTime, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base, IDMixin, MoodEnum


class MoodCategory(Base, IDMixin):
    __tablename__ = 'mood_categories'
    name: Mapped[str] = mapped_column(Text, unique=True)


class MoodLog(Base, IDMixin):
    __tablename__ = 'mood_logs'
    __table_args__ = (
        Index('ix_mood_logs_user_id', 'user_id'),
        Index('ix_mood_logs_logged_at', 'logged_at')
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    mood: Mapped[str] = mapped_column(Text)
    intensity: Mapped[int] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM, UUID
from .base import Base, IDMixin, TimestampMixin

mood_enum = ENUM('happy','calm','neutral','stressed','sad','burned_out', name='mood_enum', create_type=False)


class MoodCategory(Base, IDMixin):
    __tablename__ = 'mood_categories'
    name = Column(mood_enum, unique=True)


class MoodLog(Base, IDMixin, TimestampMixin):
    __tablename__ = 'mood_logs'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    mood = Column(mood_enum, nullable=False)
    intensity = Column(sa.Integer)
    notes = Column(sa.Text)
    logged_at = Column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
