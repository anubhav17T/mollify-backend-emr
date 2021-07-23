from utils.logger.logger import logger
from utils.connection_configuration.db_object import db
from models.payment import VerifyRazorPayment


def save_razorpay_payment(verification: VerifyRazorPayment,order_status:str):

    logger.info("##### SAVING PAYMENT IN THE RAZORPAY ORDER TABLE FUNCTION CALLED #####")
    query = "INSERT INTO razorpay_order_status VALUES (nextval('razorpay_order_status_id_seq'),:razorpay_order_id," \
            ":razorpay_payment_id,:razorpay_signature,:consultation_id,now() at time zone 'UTC',:order_status " \
            "RETURNING id "
    try:
        return db.execute(query=query, values={"razorpay_order_id": verification.razorpay_order_id,
                                               "razorpay_payment_id": verification.razorpay_payment_id,
                                               "razorpay_signature": verification.razorpay_signature,
                                               "consultation_id": verification.consultation_id,
                                               "order_status":order_status
                                               }
                          )
    except Exception as Why:
        logger.error("######### ERROR IN EXECUTING SAVE-RAZORPAY PAYEMENT DB FUNCTION {} #############".format(Why))
    finally:
        logger.info("####### EXECUTING SAVE-RAZORPAY PAYEMENT DB FUNCTION OVER ############")
