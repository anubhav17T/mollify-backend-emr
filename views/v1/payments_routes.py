from fastapi import APIRouter, Path
from fastapi import status
from models.payment import Payment, VerifyRazorPayment
from payments.razorpay.razor import PaymentRazorpay
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_consultation_function import check_if_consultation_parent_id_exist, \
    update_consultation_status
from utils.db_functions.db_payments_function import save_razorpay_payment, update_payment_status
from utils.logger.logger import logger

payment_router = APIRouter()


@payment_router.post("/razorpay/payments", tags=["PAYMENTS"], description="PAYMENT ROUTE FOR RAZORPAY", status_code=200)
async def razorpay_payment(payment: Payment):
    razorpay_client = PaymentRazorpay()
    try:
        success = razorpay_client.razorpay_client.order.create(dict(amount=payment.amount,
                                                                    currency=payment.order_currency))
        return success
    except Exception as WHY:
        return {"Exception is": str(WHY)}


@payment_router.post("/razorpay/payments/verify", tags=["PAYMENTS"],
                     description="PAYMENT VERIFICATION FOR RAZORPAY",
                     status_code=200)
async def verify_razorpay_payment(verify: VerifyRazorPayment):
    logger.info("########## CHECKING IF CONSULTATION EXIST OR NOT ############")
    success_in_consultation = await check_if_consultation_parent_id_exist(id=verify.consultation_id)

    # CHECK FOR DUPLICATE PAYMENT



    if success_in_consultation is None:
        logger.info("########## NO CONSULTATION FOUND ############")
        raise CustomExceptionHandler(message="NO CONSULTATION ID EXIST", code=status.HTTP_400_BAD_REQUEST,
                                     success=False, target="RAZORPAY-VERIFY-PAYMENT")
    logger.info("####### CONSULTATION EXIST, MOVING FORWARD FOR PAYMENT VERIFICATION ##########")
    razorpay_client_verify = PaymentRazorpay()

    try:
        params_dict = {
            'razorpay_order_id': verify.razorpay_order_id,
            'razorpay_payment_id': verify.razorpay_payment_id,
            'razorpay_signature': verify.razorpay_signature
        }
        razorpay_client_verify.razorpay_client.utility.verify_payment_signature(params_dict)
    except Exception as Why:
        logger.error("########## EXCEPTION OCCURRED IN RAZORPAY PAYMENT VERIFICATION {} ########".format(Why))
        success_in_db_execution = await save_razorpay_payment(verification=verify, order_status="NOT PAID")
        if success_in_db_execution is None:
            raise CustomExceptionHandler(message="SOMETHING WENT WRONG,ORDER NOT COMPLETED",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False, target="RAZORPAY-VERIFY-PAYMENT-DB INSERTION ERROR")
        return CustomExceptionHandler(message="Something went wrong,payment is not successful",
                                      success=False,
                                      code=status.HTTP_400_BAD_REQUEST,
                                      target="RAZORPAY-VERIFY-SIGNATURE-NOT-VALID"
                                      )
    success_in_db_execution = await save_razorpay_payment(verification=verify, order_status="PAID")
    if success_in_db_execution is None:
        raise CustomExceptionHandler(message="SOMETHING WENT WRONG,ORDER NOT COMPLETED",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False, target="RAZORPAY-VERIFY-PAYMENT-DB INSERTION ERROR")
    else:
        success = await update_consultation_status(id=verify.consultation_id)
        if success is None:
            # ROLLING BACK THE STATUS OF PAID TO UNPAID
            await update_payment_status(id=success_in_db_execution)
            raise CustomExceptionHandler(message="SOMETHING WENT WRONG,ORDER NOT COMPLETED",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False,
                                         target="RAZORPAY-VERIFY-PAYMENT-DB INSERTION ERROR")
        return {"message": "Order Completed Successfully",
                "code": status.HTTP_201_CREATED,
                "success": True
                }
