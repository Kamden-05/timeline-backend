from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from crud import user_crud
from db import get_db
from models.user_models import User, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

DbSession = Annotated[Session, Depends(get_db)]




@router.get("/me", response_model=UserRead)
def get_current_user(user_id: int, db: DbSession):
    user = user_crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return user
