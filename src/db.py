import os

from src.models import User, Timeline, Note

from sqlmodel import SQLModel, create_engine, Session
from src.config import settings

url = settings.POSTGRES_URL

engine = create_engine(url, echo=True) # type: ignore

SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as db:
        yield db