from pydantic import BaseModel, Field


class Payment(BaseModel):
    amount: float = Field(..., description="Data Field For Payment amount", gt=30)
    order_currency = Field(default="INR", description="Data Field For Order currency")


class VerifyRazorPayment(BaseModel):
    razorpay_order_id: str = Field(..., description=" RAZORPAY ORDER ID ")
    razorpay_payment_id: str = Field(..., description=" RAZORPAY PAYMENT ID ")
    razorpay_signature: str = Field(..., description=" RAZORPAY SIGNATURE ")
    consultation_id: int = Field(..., description=" CONSULTATION ID ")
    order_status:str = Field(default=None,description="ORDER STATUS, TO BE CHECKED BY SERVER")
