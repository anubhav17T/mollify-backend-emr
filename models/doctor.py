from pydantic import BaseModel, Field
from fastapi import Query
from constants.const import EMAIL_REGEX
from sqlalchemy import DateTime
from typing import Optional
from models.qualification import Qualification
from typing import List


class Doctor(BaseModel):
    username: str = Field(..., example="username")
    full_name: str = Field(..., example="name + surname")
    mail: str = Query(..., regex=EMAIL_REGEX)
    password: str = Field(None, example="test@123")
    phone_number: str
    gender: Optional[str] = "Male/Female"
    experience: str
    econsultation_fee: int
    isActive: bool = None
    isOnline: bool = None
    url: str
    follow_up_fee: int
    about: str = Field(..., example="about yourself in less than 350 words")
    qualification: List[Qualification] = None
    #slug
    #createdon


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
