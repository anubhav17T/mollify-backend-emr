from datetime import datetime, timezone

from starlette import status
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_functions import find_exist_user_id, find_exist_user, check_if_time_slot_id_exist, \
    doctor_by_name, check_for_end_time, check_for_start_time
from utils.db_functions.db_specialisation_function import check_if_id_exists
from utils.logger.logger import logger

dt = datetime.now(timezone.utc)


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
            raise CustomExceptionHandler(message="User not found for the given id",
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


class TimeslotConfiguration(object):
    def __init__(self, start_time: datetime = None, end_time: datetime = None, doctor_id: int = None):
        self.start_time = start_time
        self.end_time = end_time
        self.doctor_id = doctor_id

    def time_slot_configuration_checks(self):
        if self.start_time >= self.end_time:
            logger.error("##### ERROR = ENDTIME IS LESS THAN START TIME #####")
            raise CustomExceptionHandler(message="Your end time is less than start time!!",
                                         success=False,
                                         target="Save Timeslot",
                                         code=status.HTTP_400_BAD_REQUEST)
        if self.start_time.day != self.end_time.day:
            logger.error("##### ERROR, YOU CANNOT PROVIDE END TIME GREATER THAN 24 HOURS #####")
            raise CustomExceptionHandler(
                message="End time provided for greater than 24 hours for doctor id {}".format(str(self.doctor_id)),
                success=False,
                target="Save Timeslot",
                code=status.HTTP_400_BAD_REQUEST)

        if self.start_time.date() < dt.date():
            raise CustomExceptionHandler(
                message="Earlier date cannot be provided, Exception in doctor having id= {}".format(
                    str(self.doctor_id)),
                success=False,
                target="Save Timeslot",
                code=status.HTTP_400_BAD_REQUEST)
        return True


class CheckForConsultation(object):
    def __init__(self, time_slot_id: int, doctor_id: int, doctor_time_map: dict):
        self.time_slot_id = time_slot_id
        self.doctor_id = doctor_id
        self.doctor_time_map = doctor_time_map

    async def end_time(self):
        check_if_end_time_exist = await check_for_end_time(time_slot_config_id=self.time_slot_id,
                                                           doctor_id=self.doctor_id,
                                                           end_time=self.doctor_time_map["end_time"]
                                                           )
        if check_if_end_time_exist is not None:
            raise CustomExceptionHandler(
                message="You have consultation booked, so we can't update the timeslots {}".format(
                    self.time_slot_id),
                code=status.HTTP_400_BAD_REQUEST,
                success=False,
                target="PUT-TIMESLOT-CONFIG[HAS TIMESLOT ID]"
            )
        return True

    async def start_time(self):
        check_if_start_time_exist = await check_for_start_time(time_slot_config_id=self.time_slot_id,
                                                               doctor_id=self.doctor_id,
                                                               start_time=self.doctor_time_map["start_time"]
                                                               )
        if check_if_start_time_exist is not None:
            raise CustomExceptionHandler(
                message="You have consultation booked, so we can't update the timeslot for timeslot id {}".format(
                    self.time_slot_id),
                code=status.HTTP_400_BAD_REQUEST,
                success=False,
                target="PUT-TIMESLOT-CONFIG[HAS TIMESLOT ID]"
            )
        return True