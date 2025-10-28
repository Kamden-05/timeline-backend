from sqlmodel import Session, select
from src.models.user_models import User, UserCreate, UserUpdate
from src.crud.helpers import save
from typing import Optional


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()


def create_user(db: Session, user_create: UserCreate) -> Optional[User]:
    data = user_create.model_dump(exclude_unset=True)
    user = User(**data)

    return save(db, user)


def update_user(db: Session, user_update: UserUpdate, user_id: int) -> Optional[User]:
    user = db.get(User, user_id)
    if not user:
        return None

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    return save(db, user)


def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)

    if not user:
        return False

    db.delete(user)
    db.commit()

    return True
