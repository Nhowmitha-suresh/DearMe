from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, JSON, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import Enum as SAEnum

from app.models.base import Base, IDMixin, NotificationStatusEnum


class NotificationTemplate(Base, IDMixin):
    __tablename__ = 'notification_templates'
    name: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[Optional[str]] = mapped_column(String)
    body: Mapped[Optional[str]] = mapped_column(Text)
    template_metadata: Mapped[Optional[dict]] = mapped_column("metadata", JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)



class Notification(Base, IDMixin):
    __tablename__ = 'notifications'
    __table_args__ = (
        Index('ix_notifications_user_id', 'user_id'),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    template_id: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey('notification_templates.id'))
    message: Mapped[Optional[str]] = mapped_column(Text)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[Optional[NotificationStatusEnum]] = mapped_column(SAEnum(NotificationStatusEnum, name='notification_status_enum'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    logs: Mapped[List[NotificationLog]] = relationship('NotificationLog', back_populates='notification', cascade='all, delete-orphan')


class NotificationLog(Base, IDMixin):
    __tablename__ = 'notification_logs'
    notification_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey('notifications.id', ondelete='CASCADE'))
    provider_response: Mapped[Optional[dict]] = mapped_column(JSON)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    status: Mapped[Optional[NotificationStatusEnum]] = mapped_column(SAEnum(NotificationStatusEnum, name='notification_status_enum'))

    notification: Mapped[Notification] = relationship('Notification', back_populates='logs')

