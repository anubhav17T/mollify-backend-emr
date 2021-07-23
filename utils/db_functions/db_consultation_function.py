from utils.db_functions.raw_queries import QUERY_FOR_CONSULTATION_UTILS, QUERY_IF_REVIEW_ALREADY_EXIST, \
    QUERY_IF_CLIENT_EXIST_IN_DB, QUERY_FOR_CONSULTATION_STATES_AND_PARENT_ID
from utils.logger.logger import logger
from utils.connection_configuration.db_object import db
from datetime import datetime, timezone
from models.consultation import ConsultationTable


def save_consultation(consultation: ConsultationTable, day):
    logger.info("##### SAVING CONSULTATIONS FUNCTION CALLED #####")
    query = """INSERT INTO consultations VALUES (nextval('consultations_id_seq'),:patient_id,:doctor_id,:parent_id,
    :start_time,:end_time,:time_slot_config_id,:status,:cancel_reason,now() at time zone 'UTC',:day,:session_type)RETURNING id; """
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
                                               "day": day,
                                               "session_type": consultation.session_type
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


def fetch_all_consultation(doctor_id: int):
    logger.info("### CHECK STATUS FOR CONSULTATION STATUS ######")
    query = """SELECT u.full_name patient_name ,d.id doctor_id,d.full_name doctor_full_name,start_time,end_time,
        status,cancel_reason,c.id,c.session_type,c.parent_id FROM users u INNER JOIN consultations c ON c.patient_id=u.id INNER JOIN doctors d ON 
        d.id=c.doctor_id WHERE d.id=:doctor_id ORDER BY end_time """
    try:
        return db.fetch_all(query, values={"doctor_id": doctor_id})
    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN FETCH-CONSULTATION-STATUS {}".format(e))
    finally:
        logger.info("### EXECUTED THE FETCH-CONSULTATION-STATUS METHOD ###")


def fetch_feedback_utils(doctor_id: int, patient_id: int, consultation_id: int):
    logger.info("###### GET UTILS (DOCTOR_ID,PATIENT_ID,CONSULTATION_ID) FROM THE DB METHOD CALLED #######")
    try:
        return db.fetch_one(query=QUERY_FOR_CONSULTATION_UTILS,
                            values={"id": consultation_id, "doctor_id": doctor_id, "patient_id": patient_id})
    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN FETCH-FEEDBACK-UTILS {}".format(e))
    finally:
        logger.info("### EXECUTED THE FETCH-CONSULTATION-STATUS METHOD ###")


def find_if_review_exist(consultation_id: int):
    logger.info("######### FIND IF ALREADY REVIEW EXIST METHOD CALLED ###############")
    try:
        return db.fetch_one(query=QUERY_IF_REVIEW_ALREADY_EXIST, values={"consultation_id": consultation_id})
    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN FIND-REVIEW-ALREADY-EXIST {}".format(e))
    finally:
        logger.info("##### EXECUTED THE FETCH-CONSULTATION-STATUS METHOD #####")


def client_exist(client_id: int):
    logger.info("######## CHECK IF CLINT EXIST IN THE DATABASE #######")
    try:
        return db.fetch_one(query=QUERY_IF_CLIENT_EXIST_IN_DB, values={"id": client_id})
    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN FIND-CLIENT FROM DB {}".format(e))
    finally:
        logger.info("##### EXECUTED THE FETCH-CONSULTATION-STATUS METHOD #####")


def check_for_consultation_states(parent_id: int, doctor_id: int, patient_id: int, status: str):
    logger.info("######### CHECK IF PARENT ID AND STATUS EXIST IN THE DATABASE(TABLE-CONSULTATION) #########")
    try:
        return db.fetch_all(query=QUERY_FOR_CONSULTATION_STATES_AND_PARENT_ID, values={"parent_id": parent_id,
                                                                                       "doctor_id": doctor_id,
                                                                                       "patient_id": patient_id,
                                                                                       "status": status
                                                                                       }
                            )
    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN FINDING CONSULTATION STATES FROM DB {}".format(e))
    finally:
        logger.info("##### EXECUTED THE FINDING CONSULTATION STATES METHOD #####")


def check_for_consultation_existence(parent_id: int, doctor_id: int, patient_id: int, status: str):
    query = "SELECT id,patient_id FROM consultations WHERE doctor_id=:doctor_id AND patient_id=:patient_id AND " \
            "parent_id=:parent_id AND status=:status "
    try:
        return db.fetch_one(query=query,
                            values={"parent_id": parent_id, "doctor_id": doctor_id, "patient_id": patient_id,
                                    "status": status})
    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN CONSULTATION EXISTENCE {}".format(e))
    finally:
        logger.info("##### EXECUTED THE FINDING CONSULTATION STATES METHOD #####")


def check_for_multiple_states(parent_id: int):
    query = "SELECT id,parent_id FROM consultations WHERE parent_id=:parent_id AND (status='COMPLETED' OR " \
            "status='INPROGRESS') "
    return db.fetch_all(query=query, values={"parent_id": parent_id})


def check_for_duplicate_consultation_booking(doctor_id: int, start_time: datetime, end_time: datetime):
    query = "SELECT id,parent_id FROM consultations WHERE doctor_id=:doctor_id AND start_time=:start_time AND " \
            "end_time=:end_time AND status='OPEN'"
    return db.fetch_one(query=query, values={"doctor_id": doctor_id, "start_time": start_time, "end_time": end_time})


def check_for_open_status(parent_id: int, doctor_id: int, patient_id: int):
    query = "SELECT id,patient_id,doctor_id,parent_id,status,session_type FROM consultations " \
            "WHERE patient_id=:patient_id AND doctor_id=:doctor_id AND " \
            "id=:parent_id AND status='OPEN' "
    return db.fetch_one(query=query,
                        values={"parent_id": parent_id, "doctor_id": doctor_id, "patient_id": patient_id})


def check_if_consultation_parent_id_exist(parent_id: int):
    query = "SELECT id,doctor_id FROM consultations WHERE parent_id=:parent_id"
    return db.fetch_one(query=query,values={"parent_id":parent_id})
