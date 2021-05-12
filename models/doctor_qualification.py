from pydantic import BaseModel


class DoctorQualification(BaseModel):
    doctor_id: int
    qualification_id: int