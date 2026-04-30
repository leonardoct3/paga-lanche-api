from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from src.core.security import require_api_key
from src.database.database import get_db
from src.repositories import runs as run_repository
from src.schemas.runs import RunCreate, RunRead
from src.services import runs as run_service

router = APIRouter(
    prefix="/runs",
    tags=["runs"],
    dependencies=[Depends(require_api_key)],
)


@router.post("", response_model=RunRead, status_code=status.HTTP_201_CREATED)
def create_run(run_in: RunCreate, db: Session = Depends(get_db)):
    return run_service.create_run(db, run_in)


@router.get("", response_model=list[RunRead])
def list_runs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return run_repository.list_runs(db, skip=skip, limit=limit)


@router.get("/{run_id}", response_model=RunRead)
def get_run(run_id: int, db: Session = Depends(get_db)):
    return run_service.get_run_or_404(db, run_id)


@router.delete("/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_run(run_id: int, db: Session = Depends(get_db)):
    run_service.delete_run(db, run_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
