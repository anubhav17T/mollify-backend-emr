from utils.logger.logger import logger
from utils.connection_configuration.db_object import db
from datetime import datetime, timezone
from models.feedback import Feedback


def save_feedback(feedback: Feedback):
    logger.info("###### SAVING FEEDBACK FUNCTION CALLED ######")
    print(feedback)
    query = """INSERT INTO feedbacks VALUES (nextval('feedbacks_id_seq'),:consultation_id,:doctor_id,:patient_id,
    :wait_time_rating,:overall_rating,:review,:is_doctor_recommended,:is_doctor_active,now() at time zone 'UTC') RETURNING id; """
    logger.info("##### EXECUTION OF QUERY OF SAVE FEEDBACK")
    try:
        return db.execute(query=query, values={"consultation_id": feedback.consultation_id,
                                               "doctor_id": feedback.doctor_id,
                                               "patient_id": feedback.patient_id,
                                               "wait_time_rating": feedback.wait_time_rating,
                                               "overall_rating": feedback.overall_rating,
                                               "review": feedback.review,
                                               "is_doctor_recommended": feedback.is_doctor_recommended,
                                               "is_doctor_active": True
                                               }
                          )
    except Exception as e:
        logger.error("##### EXCEPTION IN SAVE_FEEDBACK FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### FIND SAVE_FEEDBACK FUNCTION COMPLETED ####")


def get_feedbacks():
    logger.info("##### GET FEEDBACKS OF THE DOCTORS ########")
    query = """ SELECT * FROM feedbacks """
    logger.info("##### EXECUTION OF QUERY OF GET FEEDBACK")
    try:
        return db.fetch_all(query=query)
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_FEEDBACK FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### GET_FEEDBACK FUNCTION COMPLETED ####")


def get_specific_doctor_feedback(id: int):
    logger.info("##### GET SPECIFIC DOCTOR ID FEEDBACK FUNCTION IS CALLED #######")
    query = "SELECT doctor_id,rating,description FROM feedbacks WHERE doctor_id=:doctor_id"
    try:
        return db.fetch_all(query=query, values={"doctor_id": id})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_SPECIFIC_FEEDBACK FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### GET_FEEDBACK FUNCTION COMPLETED ####")


def get_all_feedbacks(doctor_id: int):
    logger.info("##### QUERY TO GET ALL THE FEEDBACKS FOR SPECIFIC DOCTOR ###########")
    query = """SELECT users.full_name AS review_by, feedbacks.consultation_id,feedbacks.overall_rating,
    feedbacks.review,feedbacks.is_doctor_recommended,feedbacks.wait_time_rating,feedbacks.created_on AS reviewed_at,doctors.full_name AS doctor_name FROM users INNER JOIN feedbacks ON 
    feedbacks.patient_id=users.id INNER JOIN doctors ON feedbacks.doctor_id=doctors.id WHERE 
    doctor_id=:doctor_id """
    try:
        return db.fetch_all(query=query, values={"doctor_id": doctor_id})
    except Exception as e:
        logger.error("######## EXCEPTION IN GET_SPECIFIC_FEEDBACK FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("######## GET_FEEDBACK FUNCTION COMPLETED #########")


def find_if_feedback_exist(feedback_id:int):
    logger.info("######## FIND IF FEEDBACK EXIST METHOD CALLED ##################")
    try:
        query = "SELECT id,doctor_id FROM feedbacks WHERE id=:id"
        return db.fetch_one(query=query,values={"id":feedback_id})
    except Exception as why:
        logger.error("######## EXCEPTION IN GET_SPECIFIC_FEEDBACK FUNCTION IS {}".format(why))
        return False
    finally:
        logger.info("######## GET_FEEDBACK FUNCTION COMPLETED #########")


def update_feedback(query: str,values_map: dict):
    logger.info("###### UPDATING FEEDBACKS TABLE #########")
    try:
        return db.execute(query=query,values=values_map)
    except Exception as why:
        logger.error("###### EXCEPTION IN UPDATE FEEDBACK IS= {} ########".format(why))
        return False
    finally:
        logger.info("######## UPDATE FEEDBACK FUNCTION COMPLETED #########")

