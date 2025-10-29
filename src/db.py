from models import User, Timeline, Event

from sqlmodel import SQLModel, create_engine, Session
from config import settings

url = settings.POSTGRES_URL

engine = create_engine(url, echo=False)  # type: ignore

SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as db:
        yield db
