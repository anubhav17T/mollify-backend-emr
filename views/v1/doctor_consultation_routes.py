from fastapi import status, APIRouter
from constants.variable_constants import (CONSULTATION_STATUS_OPEN,
                                          CONSULTATION_STATUS_CANCELLED, \
                                          CONSULTATION_STATUS_COMPLETED,
                                          CONSULTATION_STATUS_PROGRESS,
                                          CONSULTATION_STATUS_RESCHEDULED)
from utils.db_functions.db_consultation_function import (save_consultation,
                                                         fetch_consultation_status, \
                                                         fetch_all_consultation,
                                                         check_for_consultation_states,
                                                         check_for_consultation_existence,
                                                         check_for_multiple_states, \
                                                         )
from utils.logger.logger import logger
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from models.consultation import ConsultationTable
from fastapi import Query, Path
from utils.utils_classes.classes_for_checks import (CheckUserExistence,
                                                    TimeslotConfiguration,
                                                    FindClient, \
                                                    OpenConsultationStatus)
from utils.utils_classes.consultation_return_message import ConsultationStatusMessage

doctor_consultation = APIRouter()
global doctor_id


@doctor_consultation.post("/doctors/consultations", tags=["DOCTORS/CONSULTATIONS"],
                          description="POST CALL FOR CONSULTATIONS")
async def create_consultations(consultation: ConsultationTable):
    logger.info("###### BOOK CONSULTATION METHOD CALLED ######")

    # run multiple process for all checks
    response = CheckUserExistence(_id=consultation.doctor_id, target="DOCTORS-CONSULTATION-POST")
    await response.check_if_user_id_exist()
    response_user = FindClient(client_id=consultation.patient_id)
    await response_user.find_if_client_exit()
    try:
        time_configuration_object = TimeslotConfiguration(start_time=consultation.start_time,
                                                          end_time=consultation.end_time,
                                                          doctor_id=consultation.doctor_id)
        time_configuration_object.check_if_start_time_greater_than_end_time()
        time_configuration_object.check_if_start_date_greater_than_end_date()
        time_configuration_object.check_if_start_date_valid()
        await time_configuration_object.check_if_timeslot_id_exist(timeslot_id=consultation.time_slot_config_id,
                                                                   doctor_id=consultation.doctor_id)
    except Exception as why:
        logger.error("######### ERROR IN TIMESLOT CONFIGURATION CHECKS BECAUSE {} ##############".format(why))
        raise CustomExceptionHandler(
            message="CANNOT ABLE TO VALIDATE DOCTOR TIMESLOT CONFIGURATIONS BECAUSE: {},FOR DOCTOR_ID {} ".format(
                why, consultation.doctor_id),
            success=False,
            code=status.HTTP_400_BAD_REQUEST,
            target="CONSULTATION(DOCTOR-TIMESLOT-CHECK)"
        )

    open_status_object = OpenConsultationStatus(state=CONSULTATION_STATUS_OPEN, parent_id=consultation.parent_id)
    await open_status_object.id_exist()
    await open_status_object.duplicate_open_consultation(doctor_id=consultation.doctor_id,
                                                         start_time=consultation.start_time,
                                                         end_time=consultation.end_time
                                                         )

    if (consultation.status == CONSULTATION_STATUS_CANCELLED or
        consultation.status == CONSULTATION_STATUS_COMPLETED or
        consultation.status == CONSULTATION_STATUS_PROGRESS or
        consultation.status == CONSULTATION_STATUS_RESCHEDULED) \
            and consultation.parent_id is None:
        raise CustomExceptionHandler(
            message="BOOKING ID(PARENT_ID) IS NONE",
            code=status.HTTP_400_BAD_REQUEST,
            success=False, target="CONSULTATION(PARENT_ID NONE FOR OTHER STATES)")

    if consultation.parent_id is not None:
        if consultation.status == CONSULTATION_STATUS_PROGRESS:
            logger.info(
                "########## REQUESTED CONSULTATION STATE IS PROGRESS SO PREVIOUS STATE HAS TO BE OPEN #############")
            response = await check_for_consultation_states(parent_id=consultation.parent_id,
                                                           doctor_id=consultation.doctor_id,
                                                           patient_id=consultation.patient_id,
                                                           status="OPEN"
                                                           )
            if not response:
                logger.error("########## PREVIOUS STATE IS NOT OPEN OR ERROR WITH BOOKING_ID/PARENT_ID #############")
                raise CustomExceptionHandler(
                    message="BOOKING_ID(PARENT_ID) DIDN'T MATCH OR CONSULTATION STATUS IS NOT OPEN,PLEASE CHECK "
                            "IF CONSULTATION IS BOOKED/OPEN OR NOT !!!",
                    code=status.HTTP_400_BAD_REQUEST,
                    success=False, target="CONSULTATION(STATUS_PROGRESS)")

            for config in response:
                temp = dict(config)
                if temp["id"] == consultation.parent_id and temp["status"] == "OPEN":
                    logger.info("###### STAGE-1 PARENT_ID AND STATUS-> OPEN IS VALIDATED")
                    check = await check_for_consultation_existence(parent_id=consultation.parent_id,
                                                                   patient_id=consultation.patient_id,
                                                                   doctor_id=consultation.doctor_id,
                                                                   status=CONSULTATION_STATUS_PROGRESS
                                                                   )
                    if check is not None:
                        raise CustomExceptionHandler(
                            message="CONSULTATION IS ALREADY IN PROGRESS,DUPLICATE ENTRY?",
                            code=status.HTTP_400_BAD_REQUEST,
                            success=False, target="CONSULTATION(STATUS_PROGRESS)")

        if consultation.status == CONSULTATION_STATUS_COMPLETED:
            logger.info(
                "########## REQUESTED CONSULTATION STATE IS COMPLETED SO PREVIOUS STATE HAS TO BE INPROGRESS "
                "#############")
            response = await check_for_consultation_states(parent_id=consultation.parent_id,
                                                           doctor_id=consultation.doctor_id,
                                                           patient_id=consultation.patient_id,
                                                           status="INPROGRESS")
            if not response:
                logger.error("########## PREVIOUS STATE IS NOT INPROGRESS OR ERROR WITH BOOKING_ID/PARENT_ID "
                             "#############")
                raise CustomExceptionHandler(
                    message="BOOKING ID(PARENT_ID) DIDN'T MATCH OR CONSULTATION STATUS IS NOT INPROGRESS,PLEASE CHECK "
                            "IF CONSULTATION IS BOOKED/OPEN OR NOT !!!",
                    code=status.HTTP_400_BAD_REQUEST,
                    success=False, target="CONSULTATION(STATUS_COMPLETED)")

            for config in response:
                temp = dict(config)
                print(temp)
                if temp["id"] == consultation.parent_id and temp["status"] == "INPROGRESS":
                    logger.info("###### STAGE-1 PARENT_ID AND STATUS-> INPROGRESS IS VALIDATED")
                    check = await check_for_consultation_existence(parent_id=consultation.parent_id,
                                                                   patient_id=consultation.patient_id,
                                                                   doctor_id=consultation.doctor_id,
                                                                   status=CONSULTATION_STATUS_COMPLETED
                                                                   )
                    if check is not None:
                        raise CustomExceptionHandler(
                            message="CONSULTATION IS ALREADY COMPLETED, DUPLICATE ENTRY?",
                            code=status.HTTP_400_BAD_REQUEST,
                            success=False, target="CONSULTATION(STATUS_COMPLETED)")

        if consultation.status == CONSULTATION_STATUS_CANCELLED:
            logger.info(
                "########## REQUESTED CONSULTATION STATE IS CANCELLED SO PREVIOUS STATE HAS TO BE OPEN "
                "#############")
            response = await check_for_consultation_states(parent_id=consultation.parent_id,
                                                           doctor_id=consultation.doctor_id,
                                                           patient_id=consultation.patient_id,
                                                           status="OPEN")
            if not response:
                logger.error("########## PREVIOUS STATE IS NOT INPROGRESS OR ERROR WITH BOOKING_ID/PARENT_ID "
                             "#############")
                raise CustomExceptionHandler(
                    message="BOOKING ID(PARENT_ID) DIDN'T MATCH OR CONSULTATION STATUS IS NOT OPEN,PLEASE CHECK "
                            "IF CONSULTATION IS BOOKED/OPEN OR NOT !!!",
                    code=status.HTTP_400_BAD_REQUEST,
                    success=False, target="GET-CONSULTATION")

            logger.info("########## CHECKING IF PREVIOUS STATE IS ASSOCIATED WITH ANY STATE ##########")
            response_for_states = await check_for_multiple_states(parent_id=consultation.parent_id)
            if response_for_states:
                raise CustomExceptionHandler(
                    message="BOOKING CANNOT BE CANCELLED BECAUSE IT IS EITHER COMPLETED OR INPROGRESS",
                    code=status.HTTP_400_BAD_REQUEST,
                    success=False,
                    target="CONSULTATION(STATUS_CANCELLED)"
                )
            for config in response:
                temp = dict(config)
                if temp["id"] == consultation.parent_id and temp["status"] == "OPEN":
                    logger.info("###### STAGE-1 PARENT_ID AND STATUS-> INPROGRESS IS VALIDATED")
                    if consultation.cancel_reason is None:
                        raise CustomExceptionHandler(
                            message="Can you please specify cancellation reason",
                            code=status.HTTP_400_BAD_REQUEST,
                            success=False,
                            target="CONSULTATION(STATUS_CANCELLED)"
                        )

                    check = await check_for_consultation_existence(parent_id=consultation.parent_id,
                                                                   patient_id=consultation.patient_id,
                                                                   doctor_id=consultation.doctor_id,
                                                                   status=CONSULTATION_STATUS_CANCELLED
                                                                   )
                    if check is not None:
                        raise CustomExceptionHandler(
                            message="CONSULTATION IS ALREADY CANCELLED, DUPLICATE ENTRY?",
                            code=status.HTTP_400_BAD_REQUEST,
                            success=False, target="CONSULTATION(STATUS_CANCELLED)")

    day = consultation.start_time.strftime("%A").upper()
    check_response = await save_consultation(consultation=consultation, day=day)
    if not check_response:
        raise CustomExceptionHandler(message="unable to insert in consultations table",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False, target="SAVE-CONSULTATION")
    message = ConsultationStatusMessage(status=consultation.status)
    return message.message()


@doctor_consultation.get("/doctors/consultations/{id}", tags=["DOCTORS/CONSULTATIONS"],
                         description="GET CALL FOR CONSULTATIONS")
async def get_consultations(id: int = Path(..., description="id of the doctor"),
                            checkStatus: str = Query(None, description="return status of consultations")):
    logger.info("####### GET CONSULTATION METHOD IS CALLED #########")
    global doctor_id
    response = CheckUserExistence(_id=id, target="DOCTORS-CONSULTATION-GEGTG")
    await response.check_if_user_id_exist()

    if checkStatus is None:
        logger.info("######## CHECK STATUS IS NONE, FETCHING ALL ID #########")
        check_response = await fetch_all_consultation(doctor_id=id)
        if not check_response:
            logger.error("##### UNABLE TO FIND THE CONSULTATION STATUS #########")
            raise CustomExceptionHandler(message="Unable to find consultation with status open",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False, target="GET-CONSULTATION")
        return check_response
    else:
        logger.info("###### CHECK STATUS IS {}".format(checkStatus))
        check_response = await fetch_consultation_status(status=checkStatus, doctor_id=id)
        if not check_response:
            logger.error("###### UNABLE TO FIND THE CONSULTATION STATUS #######")
            raise CustomExceptionHandler(message="Unable to find consultation with status {}".format(checkStatus),
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False, target="GET-CONSULTATION")
        return check_response
