from pydantic import BaseModel, Field


class Payment(BaseModel):
    amount:float = Field(...,description="Data Field For Payment amount",gt=30)
    payment_id:str = Field(...,description="Data Field For Payment Id")