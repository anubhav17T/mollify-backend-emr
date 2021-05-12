from models.doctor import Doctor, DoctorUpdate, ChangePassword
from fastapi import Depends
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
