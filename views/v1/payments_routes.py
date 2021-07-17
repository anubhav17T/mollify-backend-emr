from fastapi import APIRouter, Path
from fastapi import status
from models.payment import Payment
from payments.razorpay.razor import PaymentRazorpay
payment_router = APIRouter()


@payment_router.post("/razorpay/payments",tags=["PAYMENTS"],description="PAYMENT ROUTE FOR RAZORPAY",status_code=200)
async def razorpay_payment(payment: Payment):
    razorpay_client = PaymentRazorpay()
    try:
        success = razorpay_client.razorpay_client.order.create(dict(amount=payment.amount, currency=payment.order_currency))
        return success
    except Exception as WHY:
        return {"exception is":str(WHY)}