from pydantic import BaseModel, Field

class Feedback(BaseModel):
    consultation_id: int = Field(..., description="Unique ID For Consultation")
    doctor_id: int = Field(..., description="Unique id for doctor")
    patient_id: int = Field(..., description="Unique id for patient")
    wait_time_rating: float = Field(default=None, gt=0, lt=6,
                                    description="Client/Patient Opinion how long they waited for the doctor")
    overall_rating: float = Field(..., gt=0, lt=6, description="Overall Rating for the doctor")
    review: str = Field(default=None, description="Description about the therapy provided",max_length=500, min_length=40)
    is_doctor_recommended: bool = Field(..., description="Will client/patient recommend the doctor")
    is_doctor_active: bool = Field(default=True, description="Is doctor active or not")


class FeedbackUpdate(BaseModel):
    review: str = Field(default=None, description="Description about the therapy provided",max_length=500,min_length=40)
    is_doctor_recommended: bool = Field(default=None, description="Will client/patient recommend the doctor")