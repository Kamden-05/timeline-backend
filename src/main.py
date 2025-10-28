from fastapi import FastAPI
from src.routers import notes, timelines, users

app = FastAPI()

app.include_router(users.router)
app.include_router(timelines.router)
app.include_router(notes.router)
