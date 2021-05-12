from pydantic import BaseModel, Field


class Qualification(BaseModel):
    doctor_id: int = None
    qualification_name: str
    institute_name: str
    year: str
