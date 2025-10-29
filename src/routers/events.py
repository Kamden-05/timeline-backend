from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from crud import event_crud, timeline_crud
from db import get_db
from models.event_models import EventRead, EventCreate, EventUpdate
from models.user_models import User
from sqlmodel import Session
from dependencies import get_current_user

router = APIRouter(prefix="/timelines/{timeline_id}/events", tags=["events"])

DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=list[EventRead])
def get_events(
    timeline_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    timeline = timeline_crud.get_timeline(db, timeline_id)
    if not timeline or timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )
    return event_crud.get_event_by_timeline(db, timeline_id)


@router.get("/{event_id}", response_model=EventRead)
def get_event_by_id(
    timeline_id: int,
    event_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    timeline = timeline_crud.get_timeline(db, timeline_id)
    if not timeline or timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )

    event = event_crud.get_event(db, event_id)
    if not event or event.timeline_id != timeline_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found in timeline {timeline_id}",
        )
    return event


@router.post("", response_model=EventRead)
def create_note(
    timeline_id: int,
    event_create: EventCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    timeline = timeline_crud.get_timeline(db, timeline_id)
    if not timeline or timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )
    return event_crud.create_event(db, event_create, timeline_id)


@router.patch("/{event_id}", response_model=EventRead)
def update_note(
    timeline_id: int,
    event_id: int,
    event_update: EventUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    timeline = timeline_crud.get_timeline(db, timeline_id)
    if not timeline or timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )

    event = event_crud.get_event(db, event_id)
    if not event or event.timeline_id != timeline_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found in timeline {timeline_id}",
        )

    return event_crud.update_event(db, event_update, event_id)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    timeline_id: int,
    event_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    timeline = timeline_crud.get_timeline(db, timeline_id)
    if not timeline or timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )

    event = event_crud.get_event(db, event_id)
    if not event or event.timeline_id != timeline_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found in timeline {timeline_id}",
        )

    success = event_crud.delete_event(db, event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete event",
        )
    return
