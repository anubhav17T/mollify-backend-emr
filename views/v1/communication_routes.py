from fastapi import status, APIRouter, Query
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_functions import find_exist_user_id
from utils.logger.logger import logger
from utils.utils_classes.classes_for_checks import ConsultationValidity

information = APIRouter()


@information.get("/verify/consultation",tags=["INTER-MICROSERVICE"])
async def verify_consultation(consultation_id: int = Query(..., description="QUERY PARAMETER FOR CONSULTATION ID"),
                              patient_id: int = Query(..., description="PATIENT ID"),
                              doctor_id: int = Query(..., description="DOCTOR ID")):
    logger.info("############# VERIFYING CONSULTATION THAT IF CONSULTATION EXIST OR NOT ##############")
    validity = ConsultationValidity(consultation_id=consultation_id,
                                    doctor_id=doctor_id,
                                    patient_id=patient_id)
    response = await validity.consultation_utils()
    if not response:
        raise CustomExceptionHandler(message="CONSULTATION_EXIST",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False,
                                     target="Consultation Utils")
    response = await validity.review_exist()
    if not response:
        raise CustomExceptionHandler(message="REVIEW_EXIST",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False,
                                     target="Consultation Utils")

    return {"success": True, "message": "CHECKED", "code": status.HTTP_200_OK, "target": "VERIFY_CONSULTATION"}


@information.get("/verify/doctor",tags=["INTER-MICROSERVICE"])
async def verify_doctor(doctor_id: int = Query(..., description="QUERY PARAMETER FOR DOCTOR ID")):
    logger.info("######### VERIFYING THAT DOCTOR EXIST OR NOT ############")
    check = await find_exist_user_id(id=doctor_id)
    if check:
        return {"message":"Doctor Exist","code":status.HTTP_200_OK,"success":True}
    else:
        return {"message":"No doctor found for specific id",
                "success":False,
                "code":status.HTTP_400_BAD_REQUEST}