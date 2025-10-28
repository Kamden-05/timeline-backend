from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from datetime import datetime, date, timezone
from typing import Optional
from sqlalchemy import func


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str

    timelines: list["Timeline"] = Relationship(back_populates="user")

    created_at: datetime = Field(sa_column_kwargs={"server_default:": func.now()}, nullable=False)
    updated_at: datetime = Field(
        sa_column_kwargs={
            "server_default:": func.now(),
            "onupdate": func.now(),

        }, 
        nullable=False
    )


class Timeline(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="timelines")

    notes: list["Note"] = Relationship(back_populates="timeline")

    created_at: datetime = Field(
        sa_column_kwargs={"server_default:": func.now()}, nullable=False
    )
    updated_at: datetime = Field(
        sa_column_kwargs={
            "server_default:": func.now(),
            "onupdate": func.now(),
        },
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "title", name="uq_user_timeline_title"),
    )


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    note_date: date = Field(index=True)
    body: str

    timeline_id: Optional[int] = Field(default=None, foreign_key="timeline.id")
    timeline: Optional["Timeline"] = Relationship(back_populates="notes")

    created_at: datetime = Field(
        sa_column_kwargs={"server_default:": func.now()}, nullable=False
    )
    updated_at: datetime = Field(
        sa_column_kwargs={
            "server_default:": func.now(),
            "onupdate": func.now(),
        },
        nullable=False,
    )
