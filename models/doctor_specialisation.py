from pydantic import BaseModel
from typing import List


class DoctorSpecialisation(BaseModel):
    specialisation_id: List[int]
