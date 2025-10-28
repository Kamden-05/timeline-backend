from sqlmodel import Session, SQLModel


def save(db: Session, obj: SQLModel) -> SQLModel:

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except Exception:
        db.rollback()
        raise