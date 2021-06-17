from starlette import status
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.raw_queries import QUERY_FOR_GET_QUALIFICATIONS, QUERY_FOR_GET_SPECIFIC_QUALIFICATION_ID
from utils.logger.logger import logger
from utils.connection_configuration.db_object import db


def get_doc_qualifications(id):
    try:
        logger.info("###### FETCHING QUALIFICATIONS FOR THE ID {} ############".format(id))
        return db.fetch_all(query=QUERY_FOR_GET_QUALIFICATIONS, values={"doctor_id": id})
    except Exception as WHY:
        logger.error("####### EXCEPTION OCCURED IN GET-DOCTOR-QUALIFICATION METHOD {} ##########".format(WHY))
    finally:
        logger.info("###### GET DOCTOR QUALIFICATION METHOD OVER #########")


def check_if_qualification_exist(id):
    try:
        logger.info("###### FETCHING QUALIFICATIONS FOR THE ID {} ############".format(id))
        return db.fetch_one(query=QUERY_FOR_GET_SPECIFIC_QUALIFICATION_ID, values={"id": id})
    except Exception as WHY:
        logger.error("####### EXCEPTION OCCURED IN GET-DOCTOR-QUALIFICATION METHOD {} ##########".format(WHY))
    finally:
        logger.info("###### GET DOCTOR QUALIFICATION METHOD OVER #########")


def update_qualifications(query,values_map):
    try:
        logger.info("##### EXECUTING UPDATE QUALIFICATION QUERY #########")
        return db.execute(query=query,values=values_map)
    except Exception as WHY:
        logger.error("####### EXCEPTION OCCURRED IN UPDATE-DOCTOR-QUALIFICATION METHOD {} ##########".format(WHY))
        raise CustomExceptionHandler(message="Unable To Update In Qualification Table",
                                     target='DOC-GET-QUALIFICATIONS', code=status.HTTP_400_BAD_REQUEST, success=False)
    finally:
        logger.info("###### UPDATE DOCTOR QUALIFICATION METHOD OVER #########")
