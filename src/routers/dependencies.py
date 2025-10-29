import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from config import settings
from pydantic import BaseModel
from typing import Annotated, Optional
from db import get_db
from crud.user_crud import get_user
from sqlmodel import Session
from models.user_models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class TokenData(BaseModel):
    user_id: Optional[int] = None


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception

        try:
            user_id = int(sub)
        except ValueError:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
    except InvalidTokenError as e:
        raise credentials_exception

    user = get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception

    return user
