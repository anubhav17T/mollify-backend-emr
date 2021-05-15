from pydantic import BaseModel


class Specialisation(BaseModel):
    name: str


class SpecialisationsActiveState(BaseModel):
    is_active:str