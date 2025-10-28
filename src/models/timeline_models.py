from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import func

if TYPE_CHECKING:
    from src.models.user_models import User
    from src.models.note_models import Note

class Timeline(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="timelines")

    notes: list["Note"] = Relationship(back_populates="timeline")

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
        UniqueConstraint("user_id", "title", name="uq_user_timeline_title"),
    )

class TimelineBase(SQLModel):
    title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class TimelineCreate(TimelineBase):
    pass

class TimelineUpdate(SQLModel):
    title: Optional[str] = None
    start_date = Optional[str] = None
    end_date = Optional[str] = None

class TimelineRead(TimelineBase):
    id: int
    created_at: datetime
    updated_at: datetime
