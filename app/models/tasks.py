from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, Index, ForeignKey, JSON, Boolean
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
    priority: Mapped[Optional[PriorityEnum]] = mapped_column(SAEnum(PriorityEnum, name='priority_enum'))
    status: Mapped[Optional[TaskStatusEnum]] = mapped_column(SAEnum(TaskStatusEnum, name='task_status_enum'))
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('task_categories.id'))
    task_metadata: Mapped[Optional[dict]] = mapped_column("metadata", JSON)

    reminders: Mapped[List[TaskReminder]] = relationship('TaskReminder', back_populates='task', cascade='all, delete-orphan')
    comments: Mapped[List[TaskComment]] = relationship('TaskComment', back_populates='task', cascade='all, delete-orphan')


class TaskReminder(Base, IDMixin):
    __tablename__ = 'task_reminders'
    task_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    reminder_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    method: Mapped[Optional[str]] = mapped_column(String, default='push')

    task: Mapped[Task] = relationship('Task', back_populates='reminders')


class TaskComment(Base, IDMixin):
    __tablename__ = 'task_comments'
    task_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id'))
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    task: Mapped[Task] = relationship('Task', back_populates='comments')

