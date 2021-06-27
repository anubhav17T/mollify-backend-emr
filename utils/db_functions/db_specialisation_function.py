from utils.db_functions.raw_queries import QUERY_FOR_DOCTOR_SPECIALISATION_MAP, \
    QUERY_FOR_FIND_FIRST_DOCTOR_SPECIALISATION
from utils.logger.logger import logger
from utils.connection_configuration.db_object import db
from datetime import datetime, timezone


def check_if_id_exists(id):
    query = "SELECT * FROM specialisations WHERE id=:id"
    try:
        logger.info("### PROCEEDING FURTHER FOR EXECUTION OF QUERY OF GET SPECIFIC ID")
        return db.fetch_one(query, values={"id": id})
    except Exception as e:
        logger.error("error in fetching id {}".format(e))
    finally:
        logger.info("#### FIND ID METHOD OVER ######")


def update_specialisation(id, name):
    query = "UPDATE specialisations SET name=:name WHERE id=:id RETURNING id"
    try:
        return db.execute(query, values={"name": name, "id": id})
    except Exception as e:
        logger.error("### ERROR IN UPDATING SPECIALISATION {} #####".format(e))
    finally:
        logger.info("##### UPDATE SPECIALISATION METHOD OVER ####")


def update_doctor_status(query, values):
    try:
        logger.info("###### DB METHOD UPDATE DOCTOR STATUS IS CALLED #########")
        return db.execute(query=query, values=values)
    except Exception as e:
        logger.error("###### SOMETHING WENT WRONG IN UPDATE DOCTOR STATUS METHOD WITH {} #########".format(e))
    finally:
        logger.info("###### DB METHOD FOR DOCTOR_STATUS UPDATE IS FINISHED ##########")


def update_specialisation_table(var_id, name, is_active):
    if name is None:
        query = "UPDATE specialisations SET is_active=:is_active WHERE id=:id RETURNING id"
        return db.execute(query, values={"id": var_id,
                                         "is_active": is_active}
                          )
    if is_active is None:
        query = "UPDATE specialisations SET name=:name WHERE id=:id RETURNING id"
        return db.execute(query, values={"id": var_id,
                                         "name": name}
                          )
    else:
        query = "UPDATE specialisations SET name=:name,is_active=:is_active WHERE id=:id RETURNING id"
    try:
        return db.execute(query, values={"id": var_id,
                                         "name": name,
                                         "is_active": is_active}
                          )
    except Exception as e:
        logger.error("### ERROR IN UPDATING SPECIALISATION TABLE {} #####".format(e))
    finally:
        logger.info("##### UPDATE SPECIALISATION TABLE METHOD OVER ####")


def get_specialisation_of_doctor(doctor_id: int):
    return db.fetch_all(query=QUERY_FOR_DOCTOR_SPECIALISATION_MAP, values={"doctor_id": doctor_id})


def get_first_specialisation_of_doctor(doctor_id: int):
    return db.fetch_one(query=QUERY_FOR_FIND_FIRST_DOCTOR_SPECIALISATION, values={"doctor_id": doctor_id})
