from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import ProgramRecord
from .schemas import ProgramRecordCreate


def create_record(db: Session, payload: ProgramRecordCreate) -> ProgramRecord:
    record = ProgramRecord(**payload.model_dump())
    db.add(record)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ValueError(f"program_id '{payload.program_id}' already exists") from exc
    db.refresh(record)
    return record


def list_records(db: Session, department: str | None = None) -> list[ProgramRecord]:
    stmt = select(ProgramRecord).order_by(ProgramRecord.program_id)
    if department:
        stmt = stmt.where(ProgramRecord.department == department)
    return list(db.scalars(stmt).all())


def department_summary(db: Session) -> list[dict]:
    stmt = (
        select(
            ProgramRecord.department,
            func.count(ProgramRecord.id).label("programs"),
            func.sum(ProgramRecord.funding).label("total_funding"),
            func.sum(ProgramRecord.student_volunteers).label("volunteers"),
            func.avg(ProgramRecord.satisfaction).label("average_satisfaction"),
        )
        .group_by(ProgramRecord.department)
        .order_by(ProgramRecord.department)
    )
    return [
        {
            "department": row.department,
            "programs": row.programs,
            "total_funding": float(row.total_funding or 0),
            "volunteers": int(row.volunteers or 0),
            "average_satisfaction": round(float(row.average_satisfaction or 0), 2),
        }
        for row in db.execute(stmt)
    ]
