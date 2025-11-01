from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import func
from pydantic import field_validator

if TYPE_CHECKING:
    from src.models.timeline_models import Timeline


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(sa_column_kwargs={"unique": True})
    password_hash: str

    timelines: list["Timeline"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )

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

    @field_validator('email')
    def validate_email(cls, v: str) -> str:
        return v.strip().lower()


class UserCreate(UserBase):
    password: str


class UserDbCreate(UserBase):
    password_hash: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserDbUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes: True
