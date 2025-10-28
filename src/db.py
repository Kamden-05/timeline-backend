import os

from src.models import User, Timeline, Note

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()
url = os.getenv("DB_URL")

engine = create_engine(url, echo=True) # type: ignore

SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as db:
        yield db