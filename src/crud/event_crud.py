from sqlmodel import Session, select
from models.event_models import Event, EventCreate, EventUpdate
from crud.helpers import save
from typing import Optional


def get_event(db: Session, note_id: int) -> Optional[Event]:
    return db.get(Event, note_id)


def get_event_by_timeline(db: Session, timeline_id: int) -> list[Event]:
    statement = (
        select(Event)
        .where(Event.timeline_id == timeline_id)
        .order_by(Event.event_date.desc())
    )
    return db.exec(statement).all()


def create_event(db: Session, note_create: EventCreate, timeline_id: int) -> Event:
    data = note_create.model_dump(exclude_unset=True)
    event = Event(**data, timeline_id=timeline_id)

    return save(db, event)


def update_event(
    db: Session, note_update: EventUpdate, note_id: int
) -> Optional[Event]:
    event = db.get(Event, note_id)

    if not event:
        return None

    for key, value in note_update.model_dump(exclude_unset=True).items():
        setattr(event, key, value)

    return save(db, event)


def delete_event(db: Session, note_id: int) -> bool:
    event = db.get(Event, note_id)

    if not event:
        return False

    db.delete(event)
    db.commit()

    return True
