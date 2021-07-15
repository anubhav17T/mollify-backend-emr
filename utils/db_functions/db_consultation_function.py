from utils.db_functions.raw_queries import QUERY_FOR_CONSULTATION_UTILS, QUERY_IF_REVIEW_ALREADY_EXIST
from utils.logger.logger import logger
from utils.connection_configuration.db_object import db
from datetime import datetime, timezone
from models.consultation import ConsultationTable


def save_consultation(consultation: ConsultationTable,day):
    logger.info("##### SAVING CONSULTATIONS FUNCTION CALLED #####")
    query = """INSERT INTO consultations VALUES (nextval('consultations_id_seq'),:patient_id,:doctor_id,:parent_id,
    :start_time,:end_time,:time_slot_config_id,:status,:cancel_reason,now() at time zone 'UTC',:day)RETURNING id; """
    logger.info("#### EXECUTING SAVE CONSULTATION #####")
    try:
        return db.execute(query=query, values={"patient_id": consultation.patient_id,
                                               "doctor_id": consultation.doctor_id,
                                               "parent_id": consultation.parent_id,
                                               "start_time": consultation.start_time,
                                               "end_time": consultation.end_time,
                                               "time_slot_config_id": consultation.time_slot_config_id,
                                               "status": consultation.status,
                                               "cancel_reason": consultation.cancel_reason,
                                               "day":day
                                               })
    except Exception as e:
        logger.error("#### ERROR IN EXECUTING DB QUERY IS {}".format(e))
    finally:
        logger.info("#### EXECUTED SAVE CONSULTATION #######")


def fetch_consultation_status(status, doctor_id):
    logger.info("### CHECK STATUS FOR CONSULTATION STATUS ######")
    query = """SELECT u.full_name patient_name ,d.id doctor_id,d.full_name doctor_full_name,start_time,end_time,
    status,cancel_reason FROM users u INNER JOIN consultations c ON c.patient_id=u.id INNER JOIN doctors d ON 
    d.id=c.doctor_id WHERE status=:status AND d.id=:doctor_id ORDER BY end_time """
    try:
        return db.fetch_all(query, values={"status": status, "doctor_id": doctor_id})
    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN FETCH-CONSULTATION-STATUS {}".format(e))
    finally:
        logger.info("### EXECUTED THE FETCH-CONSULTATION-STATUS METHOD ###")


def fetch_all_consultation(doctor_id:int):
    logger.info("### CHECK STATUS FOR CONSULTATION STATUS ######")
    query = """SELECT u.full_name patient_name ,d.id doctor_id,d.full_name doctor_full_name,start_time,end_time,
        status,cancel_reason FROM users u INNER JOIN consultations c ON c.patient_id=u.id INNER JOIN doctors d ON 
        d.id=c.doctor_id WHERE d.id=:doctor_id ORDER BY end_time """
    try:
        return db.fetch_all(query, values={"doctor_id": doctor_id})
    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN FETCH-CONSULTATION-STATUS {}".format(e))
    finally:
        logger.info("### EXECUTED THE FETCH-CONSULTATION-STATUS METHOD ###")


def fetch_feedback_utils(doctor_id:int,patient_id:int,consultation_id:int):
    logger.info("###### GET UTILS (DOCTOR_ID,PATIENT_ID,CONSULTATION_ID) FROM THE DB METHOD CALLED #######")
    try:
        return db.fetch_one(query=QUERY_FOR_CONSULTATION_UTILS,values={"id":consultation_id,"doctor_id":doctor_id,"patient_id":patient_id})
    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN FETCH-FEEDBACK-UTILS {}".format(e))
    finally:
        logger.info("### EXECUTED THE FETCH-CONSULTATION-STATUS METHOD ###")


def find_if_review_exist(consultation_id:int):
    logger.info("######### FIND IF ALREADY REVIEW EXIST METHOD CALLED ###############")
    try:
        return db.fetch_one(query=QUERY_IF_REVIEW_ALREADY_EXIST,values={"consultation_id":consultation_id})
    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN FIND-REVIEW-ALREADY-EXIST {}".format(e))
    finally:
        logger.info("##### EXECUTED THE FETCH-CONSULTATION-STATUS METHOD #####")

