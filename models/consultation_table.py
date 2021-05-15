from pydantic import BaseModel
from datetime import datetime


class ConsultationTable(BaseModel):
    patient_id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime
    time_slot_config_id: int
    status: str  # enums ['RESCHUDLE, CANCELLED, INPROGRESS, OPEN, COMPLETED']
    reason: str
