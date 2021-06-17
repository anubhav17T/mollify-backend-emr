from utils.connection_configuration.db_object import db
from utils.db_functions.raw_queries import QUERY_FOR_FIND_ALL_LANGUAGES, QUERY_FOR_SPECIFIC_DOCTOR_LANGUAGE
from utils.logger.logger import logger


def save_qualification(values):
    try:
        query = "INSERT INTO qualifications VALUES (nextval('qualifications_id_seq'),:name," \
                ":is_active,:year) "
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF SAVE QUALIFICATION QUERY")
        return db.execute_many(query=query, values=values)
    except Exception as e:
        logger.error("####### EXCEPTION IN SAVE_QUALIFICATION IS = {}".format(e))
        return {"error":
                    {"message": "error in save qualification",
                     "code": 400,
                     "success": False
                     }
                }
    finally:
        logger.info("#### SAVE_QUALIFICATION  FUNCTION COMPLETED ####")


def get_all_languages():
    try:
        return db.fetch_all(query=QUERY_FOR_FIND_ALL_LANGUAGES)
    except Exception as WHY:
        logger.error("#### EXCEPTION IN GET-ALL-LANGUAGES DB METHOD IS {} #######".format(WHY))
    finally:
        logger.info("###### GET ALL LANGUAGE DB FUNCTION OVER #########")


def get_language_doctor(id:int):
    try:
        return db.fetch_all(query=QUERY_FOR_SPECIFIC_DOCTOR_LANGUAGE,values={"doctor_id":id})
    except Exception as WHY:
        logger.error("#### EXCEPTION IN GET-SPECIFIC-DOCTOR-LANGUAGE DB METHOD IS {} #######".format(WHY))
    finally:
        logger.info("###### GET-SPECIFIC-DOCTOR-LANGUAGE DB FUNCTION OVER #########")