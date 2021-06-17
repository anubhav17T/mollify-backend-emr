from starlette import status
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_functions import find_exist_user_id, find_exist_user, check_if_time_slot_id_exist, \
    doctor_by_name
from utils.db_functions.db_specialisation_function import check_if_id_exists
from utils.logger.logger import logger


class CheckUserExistence(object):
    def __init__(self, _id, target):
        self._id = _id
        self.target = target

    async def check_specialisation_id_exist(self):
        response = await check_if_id_exists(id=self._id)
        if response is None:
            logger.error("########### NO ID IS FOUND FOR GIVEN ID ############")
            raise CustomExceptionHandler(message="no id is found",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False,
                                         target=self.target)
        logger.info("### GOT THE USER ####")
        return response

    async def check_if_user_id_exist(self):
        response = await find_exist_user_id(id=self._id)
        if response is None:
            logger.error("########### NO USER IS FOUND FOR GIVED ID ############")
            raise CustomExceptionHandler(message="Cannot able to find the user for given id",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False,
                                         target=self.target
                                         )
        logger.info("### GOT THE USER ####")
        return response


class CheckUserByMail(object):

    def __init__(self, mail, target):
        self.mail = mail
        self.target = target

    async def find_user_by_email(self):
        response = await find_exist_user(mail=self.mail)
        if response is not None:
            logger.error("###########  USER IS ALREADY REGISTERED ############")
            raise CustomExceptionHandler(message="User is already registered with given email",
                                         code=status.HTTP_409_CONFLICT,
                                         success=False,
                                         target=self.target
                                         )
        logger.info("##### NEW USER #########")
        return response


class CheckTimeSlotId(object):
    def __init__(self, _id, target):
        self._id = _id
        self.target = target

    async def check_id_exist(self):
        response = await check_if_time_slot_id_exist(id=self._id)
        if response is None:
            logger.error("########### NO TIMESLOT IS FOUND FOR GIVEN ID ############")
            raise CustomExceptionHandler(message="no id is found",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False,
                                         target=self.target)
        logger.info("### GOT THE USER ####")
        return response


class DoctorByName(object):
    def __init__(self, name: str, target: str):
        self.name = name
        self.target = target

    async def find_doctor_by_name(self):
        response = await doctor_by_name(name=self.name)
        if not response:
            logger.error("########### NO DOCTOR FOUND FOR GIVEN NAME ############")
            raise CustomExceptionHandler(message="Sorry, No Doctor was found",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False,
                                         target=self.target)
        else:
            logger.info("##### FOUND THE USER ######")
            return response
