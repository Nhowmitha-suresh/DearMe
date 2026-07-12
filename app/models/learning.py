from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base, IDMixin


class Subject(Base, IDMixin):
    __tablename__ = 'subjects'
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id'))
    name: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)

    sessions: Mapped[list[LearningSession]] = relationship('LearningSession', back_populates='subject', cascade='all, delete-orphan')


class LearningSession(Base, IDMixin):
    __tablename__ = 'learning_sessions'
    subject_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('subjects.id', ondelete='CASCADE'))
    topic: Mapped[Optional[str]] = mapped_column(String)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    confidence: Mapped[Optional[int]] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    subject: Mapped[Subject] = relationship('Subject', back_populates='sessions')


class LearningProgress(Base, IDMixin):
    __tablename__ = 'learning_progress'
    subject_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('subjects.id', ondelete='CASCADE'))
    progress_percent: Mapped[Optional[float]] = mapped_column(Float)
    recorded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

