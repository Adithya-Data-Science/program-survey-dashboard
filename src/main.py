from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from . import models
from .database import Base, engine, get_db
from .schemas import DepartmentSummary, ProgramRecordCreate, ProgramRecordRead
from .service import create_record, department_summary, list_records

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Program Analytics API",
    version="2.0.0",
    description="Validated program records, relational persistence and stakeholder analytics.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/programs", response_model=ProgramRecordRead, status_code=status.HTTP_201_CREATED)
def add_program(payload: ProgramRecordCreate, db: Session = Depends(get_db)):
    try:
        return create_record(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/programs", response_model=list[ProgramRecordRead])
def get_programs(
    department: str | None = Query(default=None, max_length=80),
    db: Session = Depends(get_db),
):
    return list_records(db, department)


@app.get("/analytics/departments", response_model=list[DepartmentSummary])
def get_department_analytics(db: Session = Depends(get_db)):
    return department_summary(db)
