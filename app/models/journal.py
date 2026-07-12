from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Text, DateTime, Index, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import Enum as SAEnum

from app.models.base import Base, IDMixin, MoodEnum


class JournalEntry(Base, IDMixin):
    __tablename__ = 'journal_entries'
    __table_args__ = (
        Index('ix_journal_entries_user_id', 'user_id'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(Text)
    content: Mapped[Optional[str]] = mapped_column(Text)
    mood: Mapped[Optional[MoodEnum]] = mapped_column(SAEnum(MoodEnum, name='mood_enum'))
    tags: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    tags_rel: Mapped[List[JournalTag]] = relationship('JournalTag', secondary='journal_entry_tags', back_populates='entries')
    ai_analysis: Mapped[Optional[JournalAIAnalysis]] = relationship('JournalAIAnalysis', back_populates='entry', uselist=False, cascade='all, delete-orphan')


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
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    entry: Mapped[JournalEntry] = relationship('JournalEntry', back_populates='ai_analysis')

