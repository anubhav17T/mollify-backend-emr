from pydantic import BaseModel


class Feedback(BaseModel):
    consultation_id: int
    doctor_id: int
    rating: int
    description: str
