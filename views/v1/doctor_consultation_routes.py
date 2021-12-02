from fastapi import status, APIRouter, Depends
from constants.variable_constants import (
    CONSULTATION_STATUS_OPEN,
    CONSULTATION_STATUS_CANCELLED, \
    CONSULTATION_STATUS_COMPLETED,
    CONSULTATION_STATUS_PROGRESS,
    CONSULTATION_STATUS_RESCHEDULED)
from models.doctor import Doctor
from utils.db_functions.db_consultation_function import (save_consultation,
                                                         fetch_consultation_status, \
                                                         fetch_all_consultation,
                                                         check_for_consultation_states,
                                                         check_for_consultation_existence,
                                                         check_for_multiple_states,
                                                         check_for_duplicate_consultation_booking,
                                                         check_for_open_status, doctor_past_consultations,
                                                         doctor_upcoming_consultation, fetch_all_form_details,
                                                         doctor_custom_day_consultations, fetch_past_consultation_count, \
                                                         )
from utils.helper_function.misc import convert_datetime, check_for_cancellation_time
from utils.logger.logger import logger
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from models.consultation import ConsultationTable
from fastapi import Query, Path
from utils.utils_classes.classes_for_checks import (CheckUserExistence,
                                                    TimeslotConfiguration,
                                                    FindClient, \
                                                    ConsultationChecks)
from utils.utils_classes.consultation_return_message import ConsultationStatusMessage
from datetime import datetime
from utils.utils_classes.consultation_upcoming_custom import CustomConsultation
from utils.jwt_utils.jwt_utils import get_current_user, get_token_user

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
        time_configuration_object.check_if_time_and_date_is_valid()

        await time_configuration_object.check_if_timeslot_id_exist(timeslot_id=consultation.time_slot_config_id,
                                                                   doctor_id=consultation.doctor_id)
    except Exception as why:
        logger.error("######### ERROR IN TIMESLOT CONFIGURATION CHECKS BECAUSE {} ##############".format(why))
        raise CustomExceptionHandler(
            message="Something went wrong on our end,please try again later.",
            success=False,
            code=status.HTTP_409_CONFLICT,
            target="CONSULTATION(DOCTOR-TIMESLOT-CHECK),CANNOT ABLE TO VALIDATE TIMESLOT CONFIG BECAUSE {}".format(why)
        )
    if consultation.status == CONSULTATION_STATUS_OPEN and consultation.parent_id is not None:
        raise CustomExceptionHandler(
            message="We regret,there is a small error from our side,our team is working",
            code=status.HTTP_400_BAD_REQUEST,
            success=False,
            target="CONSULTATION(STATUS_OPEN AND PARENT_ID CHECK),BOOKING ID(PARENT_ID) IS NOT NONE"
        )

    if consultation.status == CONSULTATION_STATUS_OPEN and consultation.parent_id is None:
        if consultation.cancel_reason is not None:
            raise CustomExceptionHandler(
                message="Cancel reason?Please do not provide cancel reason while booking",
                code=status.HTTP_400_BAD_REQUEST,
                success=False, target="CONSULTATION STATES OPEN")

        state = ConsultationChecks()
        await state.duplicate_consultation_for_doctor(doctor_id=consultation.doctor_id,
                                                      start_time=consultation.start_time,
                                                      end_time=consultation.end_time
                                                      )
        # todo: if 2 consultation intersects for user and same consultation exist for

    if (consultation.status == CONSULTATION_STATUS_CANCELLED or
        consultation.status == CONSULTATION_STATUS_COMPLETED or
        consultation.status == CONSULTATION_STATUS_PROGRESS or
        consultation.status == CONSULTATION_STATUS_RESCHEDULED) \
            and consultation.parent_id is None:
        raise CustomExceptionHandler(
            message="We regret,there is a small error from our side,our team is working",
            code=status.HTTP_400_BAD_REQUEST,
            success=False, target="CONSULTATION(PARENT_ID NONE FOR OTHER STATES)")

    try:
        if consultation.parent_id is not None:
            if consultation.status == CONSULTATION_STATUS_PROGRESS:
                logger.info(
                    "########## REQUESTED CONSULTATION STATE IS PROGRESS SO PREVIOUS STATE HAS TO BE OPEN #############")
                response = await check_for_open_status(parent_id=consultation.parent_id,
                                                       doctor_id=consultation.doctor_id,
                                                       patient_id=consultation.patient_id
                                                       )
                if not response:
                    logger.error(
                        "########## PREVIOUS STATE IS NOT OPEN OR ERROR WITH BOOKING_ID/PARENT_ID #############")
                    raise Exception(
                        "BOOKING_ID(PARENT_ID) DIDN'T MATCH OR CONSULTATION STATUS IS NOT OPEN,PLEASE CHECK "
                        "IF CONSULTATION IS BOOKED/OPEN OR NOT !!!")
                temp = dict(response)
                if temp["session_type"] != consultation.session_type:
                    raise Exception("Session type is different in state in status inprogress")

                if consultation.cancel_reason is not None:
                    raise CustomExceptionHandler(
                        message="Cancel reason should be none",
                        code=status.HTTP_400_BAD_REQUEST,
                        success=False, target="CONSULTATION STATES INPROGRESS")

                if temp["id"] == consultation.parent_id and temp["status"] == "OPEN":
                    logger.info("###### STAGE-1 PARENT_ID AND STATUS-> OPEN IS VALIDATED")
                    check = await check_for_consultation_existence(parent_id=consultation.parent_id,
                                                                   patient_id=consultation.patient_id,
                                                                   doctor_id=consultation.doctor_id,
                                                                   status=CONSULTATION_STATUS_PROGRESS
                                                                   )
                    if check is not None:
                        raise Exception("CONSULTATION IS ALREADY IN PROGRESS,DUPLICATE ENTRY?")

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
                    raise Exception(
                        "BOOKING ID(PARENT_ID) DIDN'T MATCH OR CONSULTATION STATUS IS NOT INPROGRESS,PLEASE CHECK "
                        "IF CONSULTATION IS BOOKED/OPEN OR NOT !!!", )

                for config in response:
                    temp = dict(config)
                    if temp["session_type"] != consultation.session_type:
                        raise Exception("Session type is different in state in status completed")

                    if consultation.cancel_reason is not None:
                        raise CustomExceptionHandler(
                            message="Cancel reason should be none",
                            code=status.HTTP_400_BAD_REQUEST,
                            success=False, target="CONSULTATION STATES COMPLETED")

                    if temp["parent_id"] == consultation.parent_id and temp["status"] == "INPROGRESS":
                        logger.info("###### STAGE-1 PARENT_ID AND STATUS-> INPROGRESS IS VALIDATED")
                        check = await check_for_consultation_existence(parent_id=consultation.parent_id,
                                                                       patient_id=consultation.patient_id,
                                                                       doctor_id=consultation.doctor_id,
                                                                       status=CONSULTATION_STATUS_COMPLETED
                                                                       )
                        if check is not None:
                            raise Exception("CONSULTATION IS ALREADY COMPLETED, DUPLICATE ENTRY?")

            if consultation.status == CONSULTATION_STATUS_CANCELLED or consultation.status == CONSULTATION_STATUS_RESCHEDULED:
                logger.info(
                    "########## REQUESTED CONSULTATION STATE IS CANCELLED/RESCHEDULED SO PREVIOUS STATE HAS TO BE OPEN "
                    "#############")
                """ HERE PARENT_ID IS THE ID OF THE OPEN STATE"""
                response = await check_for_open_status(parent_id=consultation.parent_id,
                                                       doctor_id=consultation.doctor_id,
                                                       patient_id=consultation.patient_id
                                                       )
                if not response:
                    logger.error("########## PREVIOUS STATE IS NOT OPEN OR ERROR WITH BOOKING_ID/PARENT_ID "
                                 "#############")
                    raise Exception(
                        "BOOKING ID(PARENT_ID) DIDN'T MATCH OR CONSULTATION STATUS IS NOT OPEN,PLEASE CHECK "
                        "IF CONSULTATION IS BOOKED/OPEN OR NOT !!!")

                logger.info("########## CHECKING IF PREVIOUS STATE IS ASSOCIATED WITH ANY STATE ##########")
                response_for_states = await check_for_multiple_states(parent_id=consultation.parent_id)
                if response_for_states:
                    raise Exception("BOOKING CANNOT BE CANCELLED BECAUSE IT IS EITHER COMPLETED OR INPROGRESS")

                temp = dict(response)
                if temp["session_type"] != consultation.session_type:
                    raise Exception("Session type is different in state in cancelled/reschudeled")
                if consultation.status == CONSULTATION_STATUS_CANCELLED:
                    check = check_for_cancellation_time(cancel_time=temp["start_time"])
                    if not check:
                        raise Exception(".We Regret,Same Day Consultation Cancellation is not allowed")
                if temp["id"] == consultation.parent_id and temp["status"] == "OPEN":
                    logger.info("###### STAGE-1 PARENT_ID AND STATUS-> OPEN IS VALIDATED")
                    if consultation.cancel_reason is None:
                        raise Exception(",Can you please specify {} reason".format(str(consultation.status.name)))
                    check = await check_for_consultation_existence(parent_id=consultation.parent_id,
                                                                   patient_id=consultation.patient_id,
                                                                   doctor_id=consultation.doctor_id,
                                                                   status=consultation.status
                                                                   )
                    if check is not None:
                        raise Exception("CONSULTATION IS ALREADY CANCELLED/RESCHEDULED, DUPLICATE ENTRY?")
                # todo: same day consultation cancellation  not allow or money will cut !!
    except Exception as Why:
        raise CustomExceptionHandler(
            message="Something went wrong in doctor consultation booking {}".format(Why),
            code=status.HTTP_400_BAD_REQUEST,
            success=False, target="CONSULTATION(STATUS_CANCELLED)")
    else:
        day = consultation.start_time.strftime("%A").upper()
        response_id = await save_consultation(consultation=consultation, day=day)
        if not response_id:
            raise CustomExceptionHandler(message="Unable to insert in consultations table",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False, target="SAVE-CONSULTATION")
        message = ConsultationStatusMessage(status=consultation.status, id=response_id)
        return message.message()


@doctor_consultation.get("/doctors/consultations/", tags=["DOCTORS/CONSULTATIONS"],
                         description="GET CALL FOR CONSULTATIONS")
async def get_consultations(current_user: Doctor = Depends(get_current_user),
                            checkStatus: str = Query(None, description="return status of consultations")):
    logger.info("####### GET CONSULTATION METHOD IS CALLED #########")
    global doctor_id
    response = CheckUserExistence(_id=current_user["id"], target="DOCTORS-CONSULTATION-GEGTG")
    await response.check_if_user_id_exist()
    if checkStatus is None:
        logger.info("######## CHECK STATUS IS NONE, FETCHING ALL ID #########")
        check_response = await fetch_all_consultation(doctor_id=current_user["id"])
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


@doctor_consultation.get("/doctors/consultations/upcoming/", tags=["DOCTORS/CONSULTATIONS"],
                         description="GET CALL DOCTORS PREVIOUS CONSULTATIONS")
async def get_upcoming_doctor_consultations(current_user: Doctor = Depends(get_current_user)):
    logger.info("######## FETCHING UPCOMING CONSULTATIONS ###############")
    fetching_upcoming_consultations = await doctor_upcoming_consultation(doctor_id=current_user["id"])
    if not fetching_upcoming_consultations:
        return {"message": "You have no upcoming consultations booked",
                "success": True,
                "code": status.HTTP_200_OK,
                "data": []
                }
    consultation_information = []
    try:
        for values in fetching_upcoming_consultations:
            items = dict(values)
            if len(items["status"]) == 2:
                booking_upcoming_information = {"information": [
                    {
                        "status": items["status"][0],
                        "id": items["id"][0],
                        "cancel_reason": items["cancel_reason"][0],
                        "parent_id": items["parent_id"][0]
                    },
                    {
                        "status": items["status"][1],
                        "id": items["id"][1],
                        "cancel_reason": items["cancel_reason"][1],
                        "parent_id": items["parent_id"][1]
                    }
                ],
                    "patient": {"id": items["patient_id"], "name": items["patient_name"],
                                "gender": items["gender"], "marital_status": items["marital_status"]},
                    "status": items["status"][1],
                    "id": items["id"][1],
                    "cancel_reason": items["cancel_reason"][1],
                    "parent_id": items["parent_id"][1],
                }
            else:
                booking_upcoming_information = {"information": [
                    {
                        "status": items["status"][0],
                        "id": items["id"][0],
                        "cancel_reason": items["cancel_reason"][0],
                        "parent_id": items["parent_id"][0]
                    }
                ],
                    "patient": {"id": items["patient_id"], "name": items["patient_name"],
                                "gender": items["gender"], "marital_status": items["marital_status"]},
                    "status": items["status"][0],
                    "id": items["id"][0],
                    "parent_id": items["parent_id"][0],
                }
            booking_upcoming_information["start_time"] = items["start_time"]
            booking_upcoming_information["end_time"] = items["end_time"]
            booking_upcoming_information["session_type"] = items["session_type"]
            booking_upcoming_information["patient_id"] = items["patient_id"]
            document_info = await fetch_all_form_details(patient_id=items["patient_id"],
                                                         consultation_id=booking_upcoming_information["id"])
            if document_info:
                temp_array = []
                for val in document_info:
                    items = dict(val)
                    temp_array.append(
                        {"type": items["document_type"], "url": items["url"], "media_type": items["media_type"]})
                booking_upcoming_information["document"] = temp_array
            else:
                booking_upcoming_information["document"] = []
            consultation_information.append(booking_upcoming_information)
    except Exception as Why:
        raise CustomExceptionHandler(message="Something went wrong,cannot able to show upcoming consultations",
                                     code=status.HTTP_404_NOT_FOUND,
                                     success=False,
                                     target="GET-PAST-CONSULTATIONS-DUE_TO {}".format(Why)
                                     )
    else:
        return {"message": "Here,is your upcoming consultations",
                "success": True,
                "code": status.HTTP_200_OK,
                "data": consultation_information
                }


@doctor_consultation.get("/doctors/consultations/history",
                         tags=["DOCTORS/CONSULTATIONS"],
                         description="GET CALL DOCTORS PREVIOUS CONSULTATIONS")
async def get_past_doctor_consultations(size: int = Query(default=10),
                                        page: int = Query(default=0,
                                                          description="POSITION OF THE RECORDS TO START WITH"),
                                        current_user: Doctor = Depends(get_current_user)
                                        ):
    logger.info("######## FETCHING PAST CONSULTATIONS ###############")
    fetch_past_consultations = await doctor_past_consultations(doctor_id=current_user["id"], limit=size, offset=page)
    if not fetch_past_consultations:
        return {"message": "You have no past consultations",
                "success": True,
                "code": status.HTTP_200_OK,
                "data": [],
                "total": 0,
                "size": size,
                "page": page
                }
    # checking total consultations
    fetch_total_past_consultations = await fetch_past_consultation_count(doctor_id=current_user["id"])
    consultation_information = []
    try:
        for values in fetch_past_consultations:
            items = dict(values)
            if len(items["status"]) == 2:
                booking_history_information = {"information": [
                    {
                        "status": items["status"][0],
                        "id": items["id"][0],
                        "cancel_reason": items["cancel_reason"][0],
                        "parent_id": items["parent_id"][0]
                    },
                    {
                        "status": items["status"][1],
                        "id": items["id"][1],
                        "cancel_reason": items["cancel_reason"][1],
                        "parent_id": items["parent_id"][1]
                    }
                ],
                    "patient": {"id": items["patient_id"], "name": items["patient_name"],
                                "gender": items["gender"], "marital_status": items["marital_status"]},
                    "status": items["status"][1],
                    "id": items["id"][1],
                    "cancel_reason": items["cancel_reason"][1],
                    "parent_id": items["parent_id"][1],
                }
            else:
                booking_history_information = {"information": [
                    {
                        "status": items["status"][0],
                        "id": items["id"][0],
                        "cancel_reason": items["cancel_reason"][0],
                        "parent_id": items["parent_id"][0]
                    }
                ],
                    "patient": {"id": items["patient_id"], "name": items["patient_name"],
                                "gender": items["gender"],
                                "marital_status": items["marital_status"]
                                },
                    "status": items["status"][0],
                    "id": items["id"][0],
                    "parent_id": items["parent_id"][0],
                }
            booking_history_information["start_time"] = items["start_time"]
            booking_history_information["end_time"] = items["end_time"]
            booking_history_information["session_type"] = items["session_type"]
            booking_history_information["patient_id"] = items["patient_id"]
            document_info = await fetch_all_form_details(patient_id=items["patient_id"],
                                                         consultation_id=booking_history_information["parent_id"])
            if document_info:
                temp = []
                for val in document_info:
                    items = dict(val)
                    temp.append({"type": items["document_type"], "url": items["url"]})
                booking_history_information["document"] = temp
            else:
                booking_history_information["document"] = []
            consultation_information.append(booking_history_information)
    except Exception as Why:
        raise CustomExceptionHandler(message="Something went wrong,cannot able to show past consultations",
                                     code=status.HTTP_404_NOT_FOUND,
                                     success=False,
                                     target="GET-PAST-CONSULTATIONS-DUE_TO {}".format(Why)
                                     )
    else:
        return {"message": "Here,is your past consultations",
                "success": True,
                "code": status.HTTP_200_OK,
                "data": consultation_information,
                "total": fetch_total_past_consultations["count"],
                "size": size,
                "page": page
                }


# todo: NEED TO ADD PAGINATION IN THIS ROUTE THIS IS UPCOMING CONSULTATION
# open and number of consultation count
@doctor_consultation.get("/doctors/consultations/custom", tags=["DOCTORS/CONSULTATIONS"])
async def get_custom_consultations(
        field: str = Query(..., description="day/month/week CONSULTATIONS", min_length=3,
                           max_length=6),
        size: int = Query(default=10,
                          description="HOW MANY RECORDS IN PAGE CLIENT WANT"),
        page: int = Query(default=0, description="FROM WHICH ROW TO BEGIN OR SKIP"),
        current_user: Doctor = Depends(get_current_user)
):
    logger.info("########### FIELD PROVIDED IS {} #########".format(field))
    if field == "month" or field == "day" or field == "week":
        logger.info("####### FETCHING CUSTOM CONSULTATIONS #############")
        # we have changed the name
        consultations = CustomConsultation(doctor_id=current_user["id"], field=field, size=size, page=page)
        logger.info("##### CUSTOM CONSULTATION OBJECT MADE ########")
        return await consultations.fetch_information()
    raise CustomExceptionHandler(message="OOPS!! Something went wrong at our end.",
                                 target="GET_CUSTOM_CONSULTATIONS[QUERY SHOULD BE IN RANGE [week,month,day]",
                                 code=status.HTTP_400_BAD_REQUEST,
                                 success=False
                                 )