from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from crud import user_crud
from db import get_db
from models.user_models import User, UserCreate, UserRead, UserUpdate
from routers.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

DbSession = Annotated[Session, Depends(get_db)]
current_user_dep = Annotated[User, Depends(get_current_user)]

@router.get("/me", response_model=UserRead)
def get_users_me(current_user: current_user_dep):
    return current_user
