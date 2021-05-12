from pydantic import BaseModel


class DoctorSpecialisation(BaseModel):
    doctor_id: int
    specialisation_id: int