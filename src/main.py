from fastapi import FastAPI
from src.routers import notes, timelines, users

app = FastAPI()

app.include_router(users.router)
app.include_router(timelines.router)
app.include_router(notes.router)


@app.get("/")
def root():
    return {'message': "Kam's Timeline Maker!"}

@app.get("/health")
def check_health():
    return {"status: ok"}