from fastapi import status, APIRouter
from utils.db_functions.db_consultation_function import save_consultation, fetch_consultation_status, \
    fetch_all_consultation
from utils.db_functions.db_functions import find_exist_user_id, get_doctor_id
from utils.logger.logger import logger
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from models.consultation_table import ConsultationTable
from fastapi import Query, Path
from utils.utils_classes.classes_for_checks import CheckUserExistence

doctor_consultation = APIRouter()
global doctor_id


@doctor_consultation.post("/doctors/consultations", tags=["DOCTORS/CONSULTATIONS"],
                          description="POST CALL FOR CONSULTATIONS")
async def create_consultations(consultation: ConsultationTable):
    logger.info("###### BOOK CONSULTATION METHOD CALLED ######")
    # CHECK IF USER EXIST OR NOT
    response = CheckUserExistence(_id=consultation.doctor_id, target="DOCTORS-CONSULTATION-POST")
    await response.check_if_user_id_exist()
    if consultation.status == "RESCHEDULED":
        if consultation.cancel_reason is None:
            raise CustomExceptionHandler(message="please specify reschedule reason", code=status.HTTP_400_BAD_REQUEST,
                                         success=False, target="SAVE-CONSULTATION")
    check_response = await save_consultation(consultation=consultation)
    if not check_response:
        raise CustomExceptionHandler(message="unable to insert in consultations table",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False, target="SAVE-CONSULTATION")
    return {"message": "Cheers!! Your consultation has been booked", "code": status.HTTP_201_CREATED, "success": True}


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
