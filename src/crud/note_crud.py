from sqlmodel import Session, select
from src.models.note_models import Note, NoteCreate, NoteUpdate
from src.crud.helpers import save
from typing import Optional


def get_note(db: Session, note_id: int) -> Optional[Note]:
    return db.get(Note, note_id)


def get_note_by_timeline(db: Session, timeline_id: int) -> list[Note]:
    statement = (
        select(Note)
        .where(Note.timeline_id == timeline_id)
        .order_by(Note.note_date.desc())
    )
    return db.exec(statement).all()

def create_note(db: Session, note_create: NoteCreate, timeline_id: int) -> Note:
    data = note_create.model_dump(exclude_unset=True)
    note = Note(**data, timeline_id=timeline_id)

    return save(db, note)

def update_note(db: Session, note_update: NoteUpdate, note_id: int) -> Optional[Note]:
    note = db.get(Note, note_id)

    if not note:
        return None
    
    for key, value in note_update.model_dump(exclude_unset=True).items():
        setattr(note, key, value)

    return save(db, note)

def delete_note(db: Session, note_id: int) -> bool:
    note = db.get(Note, note_id)

    if not note:
        return False
    
    db.delete(note)
    db.commit()

    return True