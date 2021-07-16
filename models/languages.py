from pydantic import BaseModel
from enum import Enum

""" MAKE LANGUAGES AS ENUMS"""


class LanguagesName(str, Enum):
    hindi = "HINDI"
    english = "ENGLISH"
    punjabi = "PUNJABI"
    gujrati = "GUJRATI"
    malyalam = "MALYALAM"
    french = "FRENCH"
    konkani = "KONKANI"
    spanish = "SPANISH"
    bengali = "BENGALI"
    marathi = "MARATHI"
    tamil = "TAMIL"
    telegu = "TELEGU"


class Languages(BaseModel):
    name: LanguagesName


class LanguagesUpdate(BaseModel):
    name: LanguagesName
    is_active: bool = None


class LanguageUpdateModel(BaseModel):
    name: LanguagesName
    is_active: bool = None
