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
    body: str

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
