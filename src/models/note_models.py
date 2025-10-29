from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import func

if TYPE_CHECKING:
    from src.models.timeline_models import Timeline


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    note_date: date = Field(index=True)
    body: Optional[str] = Field(default=None)

    timeline_id: Optional[int] = Field(default=None, foreign_key="timeline.id")
    timeline: Optional["Timeline"] = Relationship(back_populates="notes")

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

class NoteBase(SQLModel):
    title: str
    note_date: date
    body: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(SQLModel):
    title: Optional[str] = None
    note_date: Optional[date] = None
    body: Optional[str] = None

class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes: True