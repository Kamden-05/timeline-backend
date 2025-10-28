from sqlmodel import Session, select
from src.models import Timeline
from datetime import datetime, timezone
from src.crud.helpers import save


def get_timeline(db: Session, timeline_id: int) -> Timeline:
    return db.get(Timeline, timeline_id)


def get_timeline_by_user(db: Session, user_id: int) -> Timeline:
    statement = select(Timeline).where(Timeline.user_id == user_id)
    return db.exec(statement).all()


def create_timeline(db: Session, timeline: Timeline) -> Timeline:
    return save(db, timeline)


def update_timeline(db: Session, timeline_id: int, new_title: str) -> Timeline:
    statement = select(Timeline).where(Timeline.id == timeline_id)
    timeline = db.exec(statement).one()

    timeline.title = new_title
    timeline.updated_at = datetime.now(timezone.utc)

    return save(db, timeline)


def delete_timeline(db: Session, timeline_id: int):
    timeline = db.get(Timeline, timeline_id)

    if not timeline:
        return False

    db.delete(timeline)
    db.commit()

    return True
