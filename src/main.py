from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, notes, timelines, users

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(timelines.router)
app.include_router(notes.router)


@app.get("/")
def root():
    return {"message": "Kam's Timeline Maker!"}


@app.get("/health")
def check_health():
    return {"status: ok"}
