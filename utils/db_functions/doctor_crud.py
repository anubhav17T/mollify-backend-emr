from models.doctor import Doctor, DoctorUpdate, ChangePassword, DoctorUpdateInformation
from fastapi import Depends

from utils.db_functions.raw_queries import QUERY_FOR_UPDATE_SLUG
from utils.jwt_utils.jwt_utils import get_current_user
from utils.connection_configuration.db_object import db
from utils.logger.logger import logger


def change_password_user(change_password_object: ChangePassword, current_user: Doctor):
    query = "UPDATE users SET password=:password WHERE mail=:mail"
    logger.info("####### CHANGING USER PASSWORD ##########")
    try:
        return db.execute(query, values={"password": change_password_object.new_password, "mail": current_user.mail})
    except Exception as e:
        logger.error("##### EXCEPTION IN CHANGING PASSWORD OF USER IS {}".format(e))


def save_black_list_token(token: str, current_user=Doctor):
    query = "INSERT INTO doctors_blacklists VALUES (:token,:mail)"
    return db.execute(query, values={"token": token, "mail": current_user.mail})


async def update_doctor_information(doctor_update: DoctorUpdateInformation,
                                    doctor_id: int,
                                    query_for_update: str,
                                    update_value_map: dict,
                                    slug_object=None) -> bool:
    async with db.transaction():
        transaction = await db.transaction()
        try:
            logger.info("####### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY FOR UPDATE DOCTORS INFORMATION #####")
            if slug_object is None:
                logger.info("###### SLUG OBJECT IS NONE ########")
                await db.execute(query=query_for_update, values=update_value_map)
            else:
                logger.info("###### SLUG OBJECT IS NOT NONE HAS VALUES ########")
                await db.execute(query=query_for_update, values=update_value_map)
                await db.execute(query=QUERY_FOR_UPDATE_SLUG, values={"slug": slug_object, "id": doctor_id})
            logger.info(
                "##### SUCCESSFULLY UPDATED IN THE DOCTOR TABLE FOR THE ID {} ###########".format(str(doctor_id)))


        except Exception as WHY:
            logger.error("######### ERROR IN THE QUERY BECAUSE {} ".format(WHY))
            logger.info("########## ROLLING BACK TRANSACTIONS #################")
            await transaction.rollback()
            return False
        else:
            logger.info("##### ALL WENT WELL COMMITTING TRANSACTION ########")
            await transaction.commit()
            logger.info("###### TRANSACTION COMMITTED AND SUCCESS TRUE FOR DOCTOR UPDATE #######")
            return True
