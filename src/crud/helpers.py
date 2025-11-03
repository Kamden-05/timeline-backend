from sqlmodel import Session, SQLModel
from sqlalchemy.exc import IntegrityError


def save(db: Session, obj: SQLModel) -> SQLModel:

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except Exception:
        db.rollback()
        raise