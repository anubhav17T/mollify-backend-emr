from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class Status(str, Enum):
    open = "OPEN"
    cancelled = "CANCELLED"
    completed = "COMPLETED"
    inprogress = "INPROGRESS"
    rescheduled = "RESCHEDULED"


class ConsultationTable(BaseModel):
    patient_id: int
    doctor_id: int
    parent_id: int = Field(None, description="CHILD ID FOR CONSULTATION BOOKING")
    start_time: datetime
    end_time: datetime
    time_slot_config_id: int
    status: Status
    cancel_reason: str = Field(None, description="WHY BOOKING IS CANCELLED")
