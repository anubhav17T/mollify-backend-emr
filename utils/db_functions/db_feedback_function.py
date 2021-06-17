from utils.logger.logger import logger
from utils.connection_configuration.db_object import db
from datetime import datetime, timezone
from models.feedback import Feedback


def save_feedback(feedback: Feedback):
    logger.info("##### SAVING FEEDBACK FUNCTION CALLED #####")
    query = """INSERT INTO feedbacks VALUES (nextval('feedbacks_id_seq'),:consultation_id,:doctor_id,:rating,
    :description,:patient_id,now() at time zone 'UTC') RETURNING id; """
    logger.info("##### EXECUTION OF QUERY OF SAVE FEEDBACK")
    try:
        return db.execute(query=query, values={"consultation_id": feedback.consultation_id,
                                               "doctor_id": feedback.doctor_id,
                                               "rating": feedback.rating,
                                               "description": feedback.description,
                                               "patient_id": feedback.patient_id
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


def get_all_feedbacks(doctor_id:int):
    logger.info("##### QUERY TO GET ALL THE FEEDBACKS FOR SPECIFIC DOCTOR ###########")
    query = """SELECT rating, description,full_name FROM feedbacks,users WHERE feedbacks.patient_id=users.id AND 
    doctor_id=:doctor_id """
    try:
        return db.fetch_all(query=query, values={"doctor_id": doctor_id})
    except Exception as e:
        logger.error("######## EXCEPTION IN GET_SPECIFIC_FEEDBACK FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("######## GET_FEEDBACK FUNCTION COMPLETED #########")


