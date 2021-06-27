from pydantic import BaseModel, Field


class Qualification(BaseModel):
    doctor_id: int = None
    qualification_name: str
    institute_name: str
    year: str


class UpdateQualification(BaseModel):
    qualification_name: str = None
    institute_name: str = None
    year: str = None


class QualificationDoctorUpdate(BaseModel):
    qualification_id:int = None
    qualification_name: str = None
    institute_name: str = None
    year: str = None