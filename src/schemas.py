from pydantic import BaseModel, ConfigDict, Field


class ProgramRecordCreate(BaseModel):
    program_id: str = Field(min_length=1, max_length=32)
    department: str = Field(min_length=1, max_length=80)
    partnership_type: str = Field(min_length=1, max_length=80)
    impact_area: str = Field(min_length=1, max_length=80)
    satisfaction: float = Field(ge=1.0, le=5.0)
    funding: float = Field(ge=0)
    student_volunteers: int = Field(ge=0)


class ProgramRecordRead(ProgramRecordCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DepartmentSummary(BaseModel):
    department: str
    programs: int
    total_funding: float
    volunteers: int
    average_satisfaction: float
