from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.repositories import runs as run_repository
from src.repositories import users as user_repository
from src.schemas.runs import RunCreate


def create_run(db: Session, run_in: RunCreate):
    user = user_repository.get_user(db, run_in.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return run_repository.create_run(db, run_in)


def get_run_or_404(db: Session, run_id: int):
    run = run_repository.get_run(db, run_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run not found.",
        )
    return run


def delete_run(db: Session, run_id: int) -> None:
    run = get_run_or_404(db, run_id)
    run_repository.delete_run(db, run)
