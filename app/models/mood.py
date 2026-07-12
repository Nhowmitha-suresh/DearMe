from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, Text, DateTime, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import Enum as SAEnum

from app.models.base import Base, IDMixin, MoodEnum


class MoodCategory(Base, IDMixin):
    __tablename__ = 'mood_categories'
    name: Mapped[MoodEnum] = mapped_column(SAEnum(MoodEnum, name='mood_enum'), unique=True)


class MoodLog(Base, IDMixin):
    __tablename__ = 'mood_logs'
    __table_args__ = (
        Index('ix_mood_logs_user_id', 'user_id'),
        Index('ix_mood_logs_logged_at', 'logged_at')
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    mood: Mapped[MoodEnum] = mapped_column(SAEnum(MoodEnum, name='mood_enum'), nullable=False)
    intensity: Mapped[int] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

