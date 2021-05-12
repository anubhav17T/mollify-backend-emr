from pydantic import BaseModel


class Diagnosis(BaseModel):
    consultation_id: int
    patient_id: int
    type: str  # enum [Manual_UPLOAD,DOCTOR]
    description: str
    title: str
    document: str
