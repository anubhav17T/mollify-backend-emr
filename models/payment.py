from pydantic import BaseModel, Field


class Payment(BaseModel):
    amount:float = Field(...,description="Data Field For Payment amount",gt=30)
    order_currency = Field(default="INR",description="Data Field For Order currency")