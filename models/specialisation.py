from pydantic import BaseModel


class Specialisation(BaseModel):
    name: str


class SpecialisationsActiveState(BaseModel):
    is_active: bool


class SpecialisationUpdate(BaseModel):
    name: str = None
    is_active: bool = None