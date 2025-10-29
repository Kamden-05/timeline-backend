from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from crud import user_crud
from db import get_db
from models.user_models import User, UserRead, UserUpdate, UserDbUpdate
from routers.dependencies import get_current_user
from security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/me", response_model=UserRead)
def get_current_user(current_user: CurrentUser):
    return current_user


@router.patch("/me", response_model=UserRead)
def update_current_user(
    user_update: UserUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    
    db_update = UserDbUpdate(**user_update.model_dump(exclude_unset=True))


    if hasattr(user_update, "password") and user_update.password:
        db_update.password_hash = get_password_hash(user_update.password)
    
    updated_user = user_crud.update_user(db, db_update, current_user.id)
    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(current_user: CurrentUser, db: DbSession):
    user = user_crud.get_user(db, user_id=current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    success = user_crud.delete_user(db, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user",
        )

    return
