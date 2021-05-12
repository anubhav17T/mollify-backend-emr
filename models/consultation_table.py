from pydantic import BaseModel
from sqlalchemy import DateTime


class ConsultationTable(BaseModel):
    patient_id: int
    doctor_id: int
    start_time: DateTime
    end_time: DateTime
    time_slot_config_id: int
    status: str  # enums ['RESCHUDLE, CANCELLED, INPROGRESS, OPEN, COMPLETED']
    reason: str
