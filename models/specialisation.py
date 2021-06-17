from pydantic import BaseModel

from enum import Enum

""" MAKE SPECIALISATIONS AS ENUMS"""


class SpecialisationName(str, Enum):
    workplace = "WORKPLACE"
    love_relationships = "LOVE-RELATIONSHIPS"
    addictions = "ADDICTIONS"
    career_academic = "CAREER/ACADEMIC"
    depression = "DEPRESSION"
    anxiety = "ANXIETY"
    self_improvement = "SELF-IMPROVEMENT"
    sleep = "SLEEP"
    stress = "STRESS"


class Specialisation(BaseModel):
    name: SpecialisationName


class SpecialisationsActiveState(BaseModel):
    is_active: bool


class SpecialisationUpdate(BaseModel):
    name: str = None
    is_active: bool = None
