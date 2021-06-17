from pydantic import BaseModel, Field


class Feedback(BaseModel):
    consultation_id: int
    doctor_id: int
    rating: int = Field(...,description="Rating of the doctor")
    description: str = Field(None,description="Description about the therapy provided")
    patient_id:int

