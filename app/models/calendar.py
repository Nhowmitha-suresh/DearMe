import sqlalchemy as sa
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin

event_type_enum = ENUM('meeting','study','assessment','interview','personal','health', name='event_type_enum', create_type=False)


class EventCategory(Base, IDMixin):
    __tablename__ = 'event_categories'
    name = Column(Text, unique=True)


class CalendarEvent(Base, IDMixin, TimestampMixin):
    __tablename__ = 'calendar_events'
    owner_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    event_type = Column(event_type_enum)
    start_at = Column(sa.TIMESTAMP(timezone=True))
    end_at = Column(sa.TIMESTAMP(timezone=True))
    location = Column(Text)
    recurring_rule = Column(Text)
    metadata = Column(sa.JSON)

    participants = relationship('EventParticipant', back_populates='event', cascade='all, delete-orphan')


class EventParticipant(Base):
    __tablename__ = 'event_participants'
    event_id = Column(UUID(as_uuid=True), sa.ForeignKey('calendar_events.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role = Column(Text)
    status = Column(Text)

    event = relationship('CalendarEvent', back_populates='participants')
