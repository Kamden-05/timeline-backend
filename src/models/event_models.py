from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import func
from sqlmodel import Field, Relationship, SQLModel, CheckConstraint

if TYPE_CHECKING:
    from src.models.timeline_models import Timeline


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    event_date: date = Field(index=True)
    body: Optional[str] = Field(default=None)

    timeline_id: Optional[int] = Field(default=None, foreign_key="timeline.id")
    timeline: Optional["Timeline"] = Relationship(back_populates="events")

    hex_color: str = Field(default="#0000FF", min_length=7, max_length=7)

    # pylint: disable=not-callable
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}, nullable=False
    )
    updated_at: datetime = Field(
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("hex_color ~ '^#[0-9A-Fa-f]{6}$'", name="valid_hex_color"),
    )


class EventBase(SQLModel):
    title: str
    event_date: date
    body: Optional[str] = None
    hex_color: str


class EventCreate(EventBase):
    pass


class EventUpdate(SQLModel):
    title: Optional[str] = None
    event_date: Optional[date] = None
    body: Optional[str] = None
    hex_color: Optional[str] = None


class EventRead(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes: True
