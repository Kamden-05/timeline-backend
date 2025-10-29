from sqlmodel import Session, select
from models.timeline_models import Timeline, TimelineCreate, TimelineUpdate
from crud.helpers import save
from typing import Optional
from sqlalchemy.exc import IntegrityError


def get_timeline(db: Session, timeline_id: int) -> Optional[Timeline]:
    return db.get(Timeline, timeline_id)


def get_timelines_by_user(db: Session, user_id: int) -> list[Timeline]:
    statement = (
        select(Timeline)
        .where(Timeline.user_id == user_id)
        .order_by(Timeline.created_at.desc())
    )
    return db.exec(statement).all()


def create_timeline(db: Session, tl_create: TimelineCreate, user_id: int) -> Optional[Timeline]:
    data = tl_create.model_dump(exclude_unset=True)
    timeline = Timeline(**data, user_id=user_id)

    try:
        return save(db, timeline)
    except IntegrityError:
        return None


def update_timeline(
    db: Session, timeline_id: int, tl_update: TimelineUpdate
) -> Optional[Timeline]:
    timeline = db.get(Timeline, timeline_id)

    if not timeline:
        return None

    for key, value in tl_update.model_dump(exclude_unset=True).items():
        setattr(timeline, key, value)

    return save(db, timeline)


def delete_timeline(db: Session, timeline_id: int) -> bool:
    timeline = db.get(Timeline, timeline_id)

    if not timeline:
        return False

    db.delete(timeline)
    db.commit()

    return True
