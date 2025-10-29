from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import func

if TYPE_CHECKING:
    from src.models.timeline_models import Timeline


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    event_date: date = Field(index=True)
    body: Optional[str] = Field(default=None)

    timeline_id: Optional[int] = Field(default=None, foreign_key="timeline.id")
    timeline: Optional["Timeline"] = Relationship(back_populates="events")

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


class EventBase(SQLModel):
    title: str
    event_date: date
    body: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventUpdate(SQLModel):
    title: Optional[str] = None
    event_date: Optional[date] = None
    body: Optional[str] = None


class EventRead(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes: True
