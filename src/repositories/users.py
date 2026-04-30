from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.user import UserCreate


def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(username=user_in.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, username: str) -> User | None:
    return db.get(User, username)


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    statement = select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(statement))


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
