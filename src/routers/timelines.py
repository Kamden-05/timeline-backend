from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from crud import timeline_crud
from db import get_db
from models.timeline_models import (
    TimelineRead,
    TimelineCreate,
    TimelineUpdate,
)
from models.user_models import User
from routers.dependencies import get_current_user
from sqlmodel import Session

router = APIRouter(prefix="/timelines", tags=["timelines"])

DbSession = Annotated[Session, Depends(get_db)]
current_user_dep = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=list[TimelineRead])
def get_timelines(current_user: current_user_dep, db: DbSession):
    timelines = timeline_crud.get_timelines_by_user(db, current_user.id)

    if timelines is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User has no timelines"
        )

    return timelines


@router.get("/{timeline_id}", response_model=TimelineRead)
def get_timeline_by_id(timeline_id: int, current_user: current_user_dep, db: DbSession):
    timeline = timeline_crud.get_timeline(db, timeline_id)

    if timeline is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timeline with id {timeline_id} not found",
        )

    if timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )

    return timeline


@router.post("", response_model=TimelineRead)
def create_timeline(
    tl_create: TimelineCreate, current_user: current_user_dep, db: DbSession
):  
    timeline = timeline_crud.create_timeline(db, tl_create, current_user.id)

    if timeline is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Timeline with title {tl_create.title} already exists"
        )

    return timeline

@router.patch("/{timeline_id}", response_model=TimelineRead)
def update_timeline(
    timeline_id: int, tl_update: TimelineUpdate, current_user: current_user_dep, db: DbSession
):
    timeline = timeline_crud.get_timeline(db, timeline_id)

    if timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )

    updated_timeline = timeline_crud.update_timeline(db, timeline_id=timeline_id, tl_update=tl_update)

    return updated_timeline


@router.delete("/{timeline_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_timeline(timeline_id: int, current_user: current_user_dep, db: DbSession):
    timeline = timeline_crud.get_timeline(db, timeline_id)

    if timeline is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timeline with id {timeline_id} not found",
        )

    if timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this timeline",
        )

    success = timeline_crud.delete_timeline(db, timeline_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete timeline",
        )

    return
