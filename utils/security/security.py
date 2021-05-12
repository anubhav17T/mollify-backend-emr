from passlib.context import CryptContext
from constants.const import BCRYPT_SCHEMA
from utils.custom_exceptions.custom_exceptions import HashPasswordError

pwd_context = CryptContext(schemes=[BCRYPT_SCHEMA])
from utils.logger.logger import logger


def hash_password(password: str):
    try:
        return pwd_context.hash(password)
    except HashPasswordError:
        logger.error("### HASHPASSWORD ERROR CANNOT ABLE TO GENERATE HASH ###")
        return False
    finally:
        logger.info("##### HASH PASSWORD FUNCTION OVER ##### ")


def verify_password(plain_password: str, hashed_passwrd: str):
    try:
        return pwd_context.verify(plain_password, hashed_passwrd)
    except ValueError:
        logger.error("### CANNOT ABLE TO VERIFY PASSWORD {} ###")
        return False
    finally:
        logger.info("#### VERIFY PASSWORD COMPLETED ##### ")


