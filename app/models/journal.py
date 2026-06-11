from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Text, DateTime, Index, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base, IDMixin


class JournalEntry(Base, IDMixin):
    __tablename__ = 'journal_entries'
    __table_args__ = (
        Index('ix_journal_entries_user_id', 'user_id'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(Text)
    content: Mapped[Optional[str]] = mapped_column(Text)
    mood: Mapped[Optional[str]] = mapped_column(Text)
    tags: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    tags_rel: Mapped[List['JournalTag']] = relationship('JournalTag', secondary='journal_entry_tags', back_populates='entries')
    ai_analysis: Mapped[List['JournalAIAnalysis']] = relationship('JournalAIAnalysis', back_populates='entry', cascade='all, delete-orphan')


class JournalTag(Base, IDMixin):
    __tablename__ = 'journal_tags'
    name: Mapped[str] = mapped_column(Text, unique=True)
    entries: Mapped[List[JournalEntry]] = relationship('JournalEntry', secondary='journal_entry_tags', back_populates='tags_rel')


class JournalEntryTag(Base):
    __tablename__ = 'journal_entry_tags'
    journal_entry_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('journal_entries.id', ondelete='CASCADE'), primary_key=True)
    tag_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('journal_tags.id', ondelete='CASCADE'), primary_key=True)


class JournalAIAnalysis(Base, IDMixin):
    __tablename__ = 'journal_ai_analysis'
    journal_entry_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('journal_entries.id', ondelete='CASCADE'), nullable=False)
    ai_summary: Mapped[Optional[str]] = mapped_column(Text)
    ai_reflection: Mapped[Optional[str]] = mapped_column(Text)
    ai_suggestions: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    entry = relationship('JournalEntry', back_populates='ai_analysis')
import sqlalchemy as sa
from sqlalchemy import Column, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin


class JournalEntry(Base, IDMixin, TimestampMixin):
    __tablename__ = 'journal_entries'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(Text)
    content = Column(Text)
    mood = Column(sa.Enum('happy','calm','neutral','stressed','sad','burned_out', name='mood_enum', create_type=False))
    tags = Column(JSON)

    ai_analysis = relationship('JournalAIAnalysis', back_populates='entry', uselist=False, cascade='all, delete-orphan')


class JournalTag(Base, IDMixin):
    __tablename__ = 'journal_tags'
    name = Column(Text, unique=True)


class JournalEntryTag(Base):
    __tablename__ = 'journal_entry_tags'
    journal_entry_id = Column(UUID(as_uuid=True), sa.ForeignKey('journal_entries.id', ondelete='CASCADE'), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), sa.ForeignKey('journal_tags.id', ondelete='CASCADE'), primary_key=True)


class JournalAIAnalysis(Base, IDMixin, TimestampMixin):
    __tablename__ = 'journal_ai_analysis'
    journal_entry_id = Column(UUID(as_uuid=True), sa.ForeignKey('journal_entries.id', ondelete='CASCADE'), nullable=False)
    ai_summary = Column(Text)
    ai_reflection = Column(Text)
    ai_suggestions = Column(JSON)

    entry = relationship('JournalEntry', back_populates='ai_analysis')
