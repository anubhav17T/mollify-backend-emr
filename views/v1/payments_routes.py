from fastapi import APIRouter, Path
from fastapi import status
from models.payment import Payment
from payments.razorpay.razor import PaymentRazorpay
payment_router = APIRouter()


@payment_router.post("/razorpay/payments",tags=["PAYMENTS"],description="PAYMENT ROUTE FOR RAZORPAY",status_code=200)
async def razorpay_payment(payment: Payment):
    razorpay_client = PaymentRazorpay()
    try:
        razorpay_client.razorpay_client.payment.capture(payment.payment_id, payment.amount)
        return {"result":razorpay_client.razorpay_client.fetch(payment.payment_id)}
    except Exception as WHY:
        return {"exception is":str(WHY)}