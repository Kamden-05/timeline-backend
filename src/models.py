from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, date
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str

    timelines = list['Timeline'] = Relationship(back_populates='user')

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Timeline(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    user_id: Optional[int] = Field(default=None, foreign_key='user.id')
    user: Optional['User'] = Relationship(back_populates='timelines')

    notes = list['Note'] = Relationship(back_populates='timeline')

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    date: date = Field(index=True)
    body: str

    timeline_id: Optional[int] = Field(default=None, foreign_key='timeline.id')
    timeline = Optional['Timeline'] = Relationship(back_populates='notes')

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)