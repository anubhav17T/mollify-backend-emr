from datetime import datetime, timezone
from starlette import status

from constants.variable_constants import CONSULTATION_STATUS_OPEN
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_consultation_function import fetch_feedback_utils, find_if_review_exist, client_exist, \
    check_for_duplicate_consultation_booking
from utils.db_functions.db_functions import find_exist_user_id, find_exist_user, check_if_time_slot_id_exist, \
    doctor_by_name, check_for_end_time, check_for_start_time, check_if_doctor_has_timeslot_id
from utils.db_functions.db_specialisation_function import check_if_id_exists
from utils.logger.logger import logger
from datetime import timedelta

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
            logger.error("########### NO USER IS FOUND FOR GIVEN ID ############")
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
    def __init__(self, start_time: datetime, end_time: datetime, doctor_id: int):
        self.start_time = start_time
        self.end_time = end_time
        self.doctor_id = doctor_id

    def check_if_start_time_greater_than_end_time(self):
        if self.start_time >= self.end_time:
            logger.error("##### ERROR = END_TIME IS LESS THAN START TIME #####")
            raise Exception("You have provided start time which is greater than end time please check")
        return True

    def check_if_start_date_greater_than_end_date(self):
        if self.start_time.day != self.end_time.day:
            logger.error("##### ERROR, YOU CANNOT PROVIDE END TIME GREATER THAN 24 HOURS #####")
            raise Exception("Start date is greater than end date, please check")
        return True

    def check_if_start_date_valid(self):
        if self.start_time.date() < dt.date():
            raise Exception("Date is not valid, please specify current or future date")
        return True

    def end_time_should_not_exceed(self):
        end = timedelta(hours=self.end_time.time().hour,
                        minutes=self.end_time.time().minute)
        max_end = timedelta(hours=23, minutes=59, seconds=50)
        if end > max_end:
            raise Exception("You have provided end time for the next date, please keep it less than 23:55")

    @staticmethod
    async def check_if_timeslot_id_exist(timeslot_id: int, doctor_id: int):
        logger.info("####### CHECKING IF TIMESLOT CONFIG ID EXIST OR NOT #################")
        response = await check_if_doctor_has_timeslot_id(doctor_id=doctor_id, timeslot_id=timeslot_id)
        if response is None:
            raise Exception("DOCTOR DO NOT SEEMS TO BE AVAILABLE AT SPECIFIED TIMESLOT ")
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
            raise Exception("You have consultation booked, so we can't update the timeslots")
        return True

    async def start_time(self):
        check_if_start_time_exist = await check_for_start_time(time_slot_config_id=self.time_slot_id,
                                                               doctor_id=self.doctor_id,
                                                               start_time=self.doctor_time_map["start_time"]
                                                               )
        if check_if_start_time_exist is not None:
            raise Exception("You have consultation booked, so we can't update the timeslot")
        return True


class ConsultationValidity(object):
    def __init__(self, doctor_id: int, patient_id: int, consultation_id: int):
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.consultation_id = consultation_id

    async def consultation_utils(self):
        response = await fetch_feedback_utils(doctor_id=self.doctor_id, patient_id=self.patient_id,
                                              consultation_id=self.consultation_id)
        if response is None:
            logger.error("##### CANNOT ABLE TO FIND THE CONSULTATION OR DOCTOR OR PATIENT ID #####")
            raise CustomExceptionHandler(message="Sorry,Either Consultation is not booked or doctor is not found",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False,
                                         target="Consultation Utils")

    async def review_exist(self):
        logger.info("####### INFO FIND IF REVIEW ALREADY EXIST ##############")
        response = await find_if_review_exist(consultation_id=self.consultation_id)
        if response:
            logger.error("##### REVIEW ALREADY THERE, YOU CANNOT ADD NEW ONE!!!! #####")
            raise CustomExceptionHandler(message="You have already provided the review for the doctor,please update "
                                                 "the previous one",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False,
                                         target="Consultation Utils")


class FindClient:
    def __init__(self, client_id: int):
        self.client_id = client_id

    async def find_if_client_exit(self):
        response = await client_exist(client_id=self.client_id)
        if response is None:
            logger.error("##### SORRY CLIENT DOESN'T EXIST WITH THIS ID!!!! #####")
            raise CustomExceptionHandler(message="Client not found for the given id",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False,
                                         target="FIND-CLIENT-ID"
                                         )
        return True


class OpenConsultationStatus:
    def __init__(self, state: str, parent_id: int = None):
        self.state = state
        self.parent_id = parent_id

    def id_exist(self):
        logger.info("########## CHECKING IF STATUS IS OPEN AND PARENT ID IS NONE #########")
        if self.state == CONSULTATION_STATUS_OPEN and self.parent_id is not None:
            raise CustomExceptionHandler(
                message="BOOKING ID(PARENT_ID) SHOULD BE NONE WHILE BOOKING CONSULTATION",
                code=status.HTTP_400_BAD_REQUEST,
                success=False, target="CONSULTATION(STATUS_OPEN AND PARENT_ID CHECK)")
        return True

    def duplicate_open_consultation(self, doctor_id: int, start_time: datetime, end_time: datetime):
        if self.state == CONSULTATION_STATUS_OPEN and self.parent_id is None:
            duplicate = check_for_duplicate_consultation_booking(doctor_id=doctor_id,
                                                                 start_time=start_time,
                                                                 end_time=end_time
                                                                 )
            if duplicate is not None:
                raise CustomExceptionHandler(
                    message="BOOKING ALREADY EXIST FOR THE SPECIFIED DOCTOR AT GIVEN TIME",
                    code=status.HTTP_400_BAD_REQUEST,
                    success=False, target="CONSULTATION(STATUS_OPEN AND PARENT_ID DUPLICATE CHECK)")
            return True
