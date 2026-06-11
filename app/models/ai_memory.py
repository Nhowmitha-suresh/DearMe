from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base, IDMixin


class AIMemory(Base, IDMixin):
    __tablename__ = 'ai_memories'
    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    memory_type: Mapped[Optional[str]] = mapped_column(String)
    content: Mapped[Optional[str]] = mapped_column(Text)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)
    embedding_id: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AIRecommendation(Base, IDMixin):
    __tablename__ = 'ai_recommendations'
    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    recommendation: Mapped[Optional[str]] = mapped_column(Text)
    source: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AIConversation(Base, IDMixin):
    __tablename__ = 'ai_conversations'
    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    topic: Mapped[Optional[str]] = mapped_column(String)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    messages = relationship('AIConversationMessage', back_populates='conversation', cascade='all, delete-orphan')


class AIConversationMessage(Base, IDMixin):
    __tablename__ = 'ai_conversation_messages'
    conversation_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('ai_conversations.id', ondelete='CASCADE'))
    sender: Mapped[Optional[str]] = mapped_column(String)
    message: Mapped[Optional[str]] = mapped_column(Text)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    conversation = relationship('AIConversation', back_populates='messages')
import sqlalchemy as sa
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin


class AIMemory(Base, IDMixin, TimestampMixin):
    __tablename__ = 'ai_memories'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'))
    memory_type = Column(Text)
    content = Column(Text)
    metadata = Column(sa.JSON)
    embedding_id = Column(Text)


class AIRecommendation(Base, IDMixin, TimestampMixin):
    __tablename__ = 'ai_recommendations'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'))
    recommendation = Column(Text)
    source = Column(sa.JSON)


class AIConversation(Base, IDMixin, TimestampMixin):
    __tablename__ = 'ai_conversations'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'))
    topic = Column(Text)
    started_at = Column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    ended_at = Column(sa.TIMESTAMP(timezone=True))

    messages = relationship('AIConversationMessage', back_populates='conversation', cascade='all, delete-orphan')


class AIConversationMessage(Base, IDMixin, TimestampMixin):
    __tablename__ = 'ai_conversation_messages'
    conversation_id = Column(UUID(as_uuid=True), sa.ForeignKey('ai_conversations.id', ondelete='CASCADE'))
    sender = Column(Text)
    message = Column(Text)
    metadata = Column(sa.JSON)

    conversation = relationship('AIConversation', back_populates='messages')
