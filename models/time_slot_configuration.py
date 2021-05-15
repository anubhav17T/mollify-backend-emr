from pydantic import BaseModel, Field
from datetime import datetime, timedelta

""" MAKE DAYS AS ENUMS"""


class TimeSlot(BaseModel):
    day: str
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
