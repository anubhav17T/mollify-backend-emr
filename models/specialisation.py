from pydantic import BaseModel


class Specialisation(BaseModel):
    name: str
    is_active: str
