from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class ProgramRecord(Base):
    __tablename__ = "program_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    program_id: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    department: Mapped[str] = mapped_column(String(80), nullable=False)
    partnership_type: Mapped[str] = mapped_column(String(80), nullable=False)
    impact_area: Mapped[str] = mapped_column(String(80), nullable=False)
    satisfaction: Mapped[float] = mapped_column(Float, nullable=False)
    funding: Mapped[float] = mapped_column(Float, nullable=False)
    student_volunteers: Mapped[int] = mapped_column(Integer, nullable=False)
