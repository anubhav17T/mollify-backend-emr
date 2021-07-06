from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from enum import Enum

""" MAKE DAYS AS ENUMS"""


class Status(str, Enum):
    sunday = "SUNDAY"
    monday = "MONDAY"
    tuesday = "TUESDAY"
    wednesday = "WEDNESDAY"
    thrusday = "THURSDAY"
    friday = "FRIDAY"
    saturday = "SATURDAY"


class TimeSlot(BaseModel):
    day: Status
    video: bool
    audio: bool
    chat: bool
    start_time: datetime = Field(..., example="2021-05-15 20:20:00 [YYYY-MM-DD HOUR:MINUTES:SS]")
    end_time: datetime = Field(..., example="2021-05-15 20:20 [YYYY-MM-DD HOUR:MINUTES]")
    video_frequency: int
    audio_frequency: int
    chat_frequency: int
    is_available: bool = None
    non_availability_reason: str = None
    is_active: bool = None
    buffer_time:int = Field(...)


class TimeSlotUpdate(BaseModel):
    id: int = None
    day: Status = None
    video: bool = None
    audio: bool = None
    chat: bool = None
    start_time: datetime = Field(None, example="2021-05-15 20:20:00 [YYYY-MM-DD HOUR:MINUTES:SS]")
    end_time: datetime = Field(None, example="2021-05-15 20:20 [YYYY-MM-DD HOUR:MINUTES]")
    video_frequency: int = None
    audio_frequency: int = None
    chat_frequency: int = None
    is_available: bool = None
    non_availability_reason: str = None
    is_active: bool = None
    buffer_time: int = None
