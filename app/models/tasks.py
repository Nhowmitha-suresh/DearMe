from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, Index, ForeignKey, JSON
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import Enum as SAEnum

from app.models.base import Base, IDMixin, AuditMixin, TaskStatusEnum, PriorityEnum


class TaskCategory(Base, IDMixin):
    __tablename__ = 'task_categories'
    name: Mapped[str] = mapped_column(String, unique=True)


class Task(Base, IDMixin, AuditMixin):
    __tablename__ = 'tasks'
    __table_args__ = (
        Index('ix_tasks_user_id', 'user_id'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    priority: Mapped[Optional[str]] = mapped_column(SAEnum(PriorityEnum, name='priority_enum'))
    status: Mapped[Optional[str]] = mapped_column(SAEnum(TaskStatusEnum, name='task_status_enum'))
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('task_categories.id'))
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    reminders: Mapped[List['TaskReminder']] = relationship('TaskReminder', back_populates='task', cascade='all, delete-orphan')
    comments: Mapped[List['TaskComment']] = relationship('TaskComment', back_populates='task', cascade='all, delete-orphan')


class TaskReminder(Base, IDMixin):
    __tablename__ = 'task_reminders'
    task_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    reminder_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    method: Mapped[Optional[str]] = mapped_column(String, default='push')

    task = relationship('Task', back_populates='reminders')


class TaskComment(Base, IDMixin):
    __tablename__ = 'task_comments'
    task_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id'))
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    task = relationship('Task', back_populates='comments')
import sqlalchemy as sa
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin

priority_enum = ENUM('low','medium','high','critical', name='priority_enum', create_type=False)
task_status_enum = ENUM('todo','in_progress','blocked','done','archived', name='task_status_enum', create_type=False)


class TaskCategory(Base, IDMixin):
    __tablename__ = 'task_categories'
    name = Column(Text, unique=True)


class Task(Base, IDMixin, TimestampMixin):
    __tablename__ = 'tasks'
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    priority = Column(priority_enum, server_default='medium')
    status = Column(task_status_enum, server_default='todo')
    due_date = Column(sa.TIMESTAMP(timezone=True))
    completed_at = Column(sa.TIMESTAMP(timezone=True))
    category_id = Column(UUID(as_uuid=True), sa.ForeignKey('task_categories.id'))
    metadata = Column(sa.JSON)

    reminders = relationship('TaskReminder', back_populates='task', cascade='all, delete-orphan')
    comments = relationship('TaskComment', back_populates='task', cascade='all, delete-orphan')


class TaskReminder(Base, IDMixin, TimestampMixin):
    __tablename__ = 'task_reminders'
    task_id = Column(UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    reminder_at = Column(sa.TIMESTAMP(timezone=True), nullable=False)
    method = Column(Text, default='push')

    task = relationship('Task', back_populates='reminders')


class TaskComment(Base, IDMixin, TimestampMixin):
    __tablename__ = 'task_comments'
    task_id = Column(UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))
    comment = Column(Text)

    task = relationship('Task', back_populates='comments')
