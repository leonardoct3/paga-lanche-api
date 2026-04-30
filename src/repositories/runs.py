from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.runs import Run
from src.schemas.runs import RunCreate


def create_run(db: Session, run_in: RunCreate) -> Run:
    run = Run(
        username=run_in.username,
        score=run_in.score,
        duration=run_in.duration,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def get_run(db: Session, run_id: int) -> Run | None:
    return db.get(Run, run_id)


def list_runs(db: Session, skip: int = 0, limit: int = 100) -> list[Run]:
    statement = select(Run).order_by(Run.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(statement))


def list_runs_by_user(
    db: Session,
    username: str,
    skip: int = 0,
    limit: int = 100,
) -> list[Run]:
    statement = (
        select(Run)
        .where(Run.username == username)
        .order_by(Run.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(statement))


def delete_run(db: Session, run: Run) -> None:
    db.delete(run)
    db.commit()
