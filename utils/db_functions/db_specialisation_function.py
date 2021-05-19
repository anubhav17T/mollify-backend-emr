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