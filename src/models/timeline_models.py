from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import func
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from models.event_models import Event
    from src.models.user_models import User


class Timeline(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="timelines")

    events: list["Event"] = Relationship(
        back_populates="timeline", sa_relationship_kwargs={"cascade": "all, delete"}
    )

    is_public: bool = Field(default=False)

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
        UniqueConstraint("user_id", "title", name="uq_user_timeline_title"),
    )


class TimelineBase(SQLModel):
    title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_public: bool = False


class TimelineCreate(TimelineBase):
    pass


class TimelineUpdate(SQLModel):
    title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_public: Optional[bool] = None


class TimelineRead(TimelineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes: True
