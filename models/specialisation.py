from pydantic import BaseModel


class Specialisation(BaseModel):
    name: str
    active: str
