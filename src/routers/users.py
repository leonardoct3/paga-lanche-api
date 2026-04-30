from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from src.core.security import require_api_key
from src.database.database import get_db
from src.repositories import runs as run_repository
from src.repositories import users as user_repository
from src.schemas.runs import RunRead
from src.schemas.user import UserCreate, UserRead
from src.services import users as user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_api_key)],
)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_in)


@router.get("", response_model=list[UserRead])
def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return user_repository.list_users(db, skip=skip, limit=limit)


@router.get("/{username}", response_model=UserRead)
def get_user(username: str, db: Session = Depends(get_db)):
    return user_service.get_user_or_404(db, username)


@router.get("/{username}/runs", response_model=list[RunRead])
def list_user_runs(
    username: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    user_service.get_user_or_404(db, username)
    return run_repository.list_runs_by_user(db, username, skip=skip, limit=limit)


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str, db: Session = Depends(get_db)):
    user_service.delete_user(db, username)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
