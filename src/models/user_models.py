from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import func

if TYPE_CHECKING:
    from src.models.timeline_models import Timeline


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(sa_column_kwargs={"unique": True})
    password_hash: str

    timelines: list["Timeline"] = Relationship(back_populates="user")

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


class UserBase(SQLModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserDbCreate(UserBase):
    password_hash: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
