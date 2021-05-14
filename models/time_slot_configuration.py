from pydantic import BaseModel
from sqlalchemy import DateTime

""" MAKE DAYS AS ENUMS"""


class TimeSlot(BaseModel):
    day: str
    video: bool
    audio: bool
    chat: bool
    start_time: DateTime
    end_time: DateTime
    video_frequency: int
    audio_frequency: int
    chat_frequency: int
    is_available: bool
    non_availability_reason: str = None
    is_active: bool
