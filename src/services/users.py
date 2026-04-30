from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.repositories import users as user_repository
from src.schemas.user import UserCreate


def create_user(db: Session, user_in: UserCreate):
    existing_user = user_repository.get_user(db, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )

    return user_repository.create_user(db, user_in)


def get_user_or_404(db: Session, username: str):
    user = user_repository.get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


def delete_user(db: Session, username: str) -> None:
    user = get_user_or_404(db, username)
    user_repository.delete_user(db, user)
