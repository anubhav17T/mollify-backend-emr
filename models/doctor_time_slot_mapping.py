from pydantic import BaseModel


class DoctorTimeSlotMapping(BaseModel):
    doctor_id: int
    time_slot_id: int
