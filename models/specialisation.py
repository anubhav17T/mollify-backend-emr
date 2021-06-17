from pydantic import BaseModel

""" MAKE SPECIALISATIONS AS ENUMS"""


class Specialisation(BaseModel):
    name: str


class SpecialisationsActiveState(BaseModel):
    is_active: bool


class SpecialisationUpdate(BaseModel):
    name: str = None
    is_active: bool = None
