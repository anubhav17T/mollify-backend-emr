from pydantic import BaseModel, Field


class Feedback(BaseModel):
    consultation_id: int = Field(..., description="Unique ID For Consultation")
    doctor_id: int = Field(..., description="Unique id for doctor")
    patient_id: int = Field(..., description="Unique id for patient")
    wait_time_rating: float = Field(None, gt=0, lt=6,
                                    description="Client/Patient Opinion how long they waited for the doctor")
    overall_rating: float = Field(..., gt=0, lt=6, description="Overall Rating for the doctor")
    review: str = Field(None, description="Description about the therapy provided")
    is_doctor_recommended: bool = Field(..., description="Will client/patient recommend the doctor")
    is_doctor_active: bool = Field(default=True, description="Is doctor active or not")


class FeedbackUpdate(BaseModel):
    review: str = Field(None, description="Description about the therapy provided")
    is_doctor_recommended: bool = Field(None, description="Will client/patient recommend the doctor")
