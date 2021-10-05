from enum import Enum
from pydantic import BaseModel, Field, validator
from fastapi import Query
from constants.const import EMAIL_REGEX
from sqlalchemy import DateTime
from typing import Optional, Dict
from models.qualification import Qualification, QualificationDoctorUpdate
from typing import List


class Gender(str, Enum):
    male = "MALE"
    female = "FEMALE"
    other = "OTHER"


class ConsultationSpecificFee(BaseModel):
    chat: int
    audio: int
    video: int


class Doctor(BaseModel):
    full_name: str = Field(..., example="name + surname")
    mail: str = Query(..., regex=EMAIL_REGEX, example="john.doe@gmail.com")
    password: str = Field(None, example="test@123")
    phone_number: str
    gender: Gender
    experience: str
    is_active: bool = None
    is_online: bool = None
    url: str = None
    about: str = Field(..., example="about yourself in less than 300 words", max_length=300)
    qualification: List[Qualification] = None
    specialisation: List[int] = None
    languages: List[int]
    consultation_charges: ConsultationSpecificFee


class DoctorResponse(BaseModel):
    username: str
    first_name: str
    last_name: str


class DoctorAvailibility(BaseModel):
    mail: str
    username: str


class ForgotPassword(BaseModel):
    mail: Optional[str]
    phone_number: Optional[str]


class ResetPassword(BaseModel):
    reset_password_token: str
    new_password: str
    confirm_password: str


class DoctorUpdate(BaseModel):
    full_name: Optional[str]
    phone_number: Optional[str]


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class DoctorImageUrl(BaseModel):
    username: str
    url: str


class DoctorLogin(BaseModel):
    through: str
    username: str
    password: str


class ChannelName(BaseModel):
    channel_name: str


class DoctorId(BaseModel):
    doctor_id: int


class DoctorStatus(BaseModel):
    is_active: bool = None
    is_online: bool = None


class DoctorUpdateInformation(BaseModel):
    full_name: str = None
    phone_number: str = None
    gender: Gender = None
    experience: str = None
    econsultation_fee: int = None
    is_active: bool = None
    is_online: bool = None
    follow_up_fee: int = None
    about: str = None
    url: str = None
    qualification: List[QualificationDoctorUpdate] = None
    specialisation: List[int] = None
    languages: List[int] = None
