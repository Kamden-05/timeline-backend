from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from crud import note_crud, timeline_crud
from db import get_db
from models.note_models import NoteRead, NoteCreate, NoteUpdate
from models.user_models import User
from sqlmodel import Session
from routers.dependencies import get_current_user

router = APIRouter(prefix="/timelines/{timeline_id}/notes", tags=["notes"])

DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=list[NoteRead])
def get_notes(
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
    return note_crud.get_note_by_timeline(db, timeline_id)


@router.get("/{note_id}", response_model=NoteRead)
def get_note_by_id(
    timeline_id: int,
    note_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    timeline = timeline_crud.get_timeline(db, timeline_id)
    if not timeline or timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )

    note = note_crud.get_note(db, note_id)
    if not note or note.timeline_id != timeline_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found in timeline {timeline_id}",
        )
    return note


@router.post("", response_model=NoteRead)
def create_note(
    timeline_id: int,
    note_create: NoteCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    timeline = timeline_crud.get_timeline(db, timeline_id)
    if not timeline or timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )
    return note_crud.create_note(db, note_create, timeline_id)


@router.patch("/{note_id}", response_model=NoteRead)
def update_note(
    timeline_id: int,
    note_id: int,
    note_update: NoteUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    timeline = timeline_crud.get_timeline(db, timeline_id)
    if not timeline or timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )

    note = note_crud.get_note(db, note_id)
    if not note or note.timeline_id != timeline_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found in timeline {timeline_id}",
        )

    return note_crud.update_note(db, note_update, note_id)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    timeline_id: int,
    note_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    timeline = timeline_crud.get_timeline(db, timeline_id)
    if not timeline or timeline.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timeline",
        )

    note = note_crud.get_note(db, note_id)
    if not note or note.timeline_id != timeline_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found in timeline {timeline_id}",
        )

    success = note_crud.delete_note(db, note_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete note",
        )
    return
