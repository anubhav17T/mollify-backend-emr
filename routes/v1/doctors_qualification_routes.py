from fastapi import APIRouter, Path
from fastapi import status

from models.qualification import UpdateQualification
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_qualifications_function import get_doc_qualifications, check_if_qualification_exist, \
    update_qualifications
from utils.db_functions.raw_queries import WHERE_ID_QUALIFICATIONS
from utils.descriptions import DESCRIPTION_FOR_QUALIFICATION_GET
from utils.logger.logger import logger
from utils.utils_classes.classes_for_checks import CheckUserExistence

doctor_qualification_router = APIRouter()


@doctor_qualification_router.get("/doctors/qualifications/{doc_id}",
                                 tags=["DOCTORS/QUALIFICATIONS"],
                                 description="Get call for qualifications ")
async def get_doctor_qualifications(
        doc_id: int = Path(..., description='PATH PARAM TO GET THE SPECIFIC QUALIFICATION')):
    logger.info("##### GET DOCTOR/QUALIFICATION API CALLED ########")
    response = CheckUserExistence(_id=doc_id, target="QUALIFICATION-GET")
    logger.info("##### FINDING THE DOCTOR/THERAPIST ID ############")
    await response.check_if_user_id_exist()
    try:
        return await get_doc_qualifications(id=doc_id)
    except Exception as WHY:
        logger.error("###### ERROR IN GET-DOCTOR QUALIFICATIONS API {} #########".format(WHY))
        raise CustomExceptionHandler(message="Unable to fetch the qualifications",
                                     target='DOC-GET-QUALIFICATIONS', code=status.HTTP_400_BAD_REQUEST, success=False)
    finally:
        logger.info("##### GET DOCTOR QUALIFICATION API OVER ############")


@doctor_qualification_router.patch("/doctors/qualifications/{id}",
                                   tags=["DOCTORS/QUALIFICATIONS"],
                                   description="Patch call for qualifications")
async def update_qualifications_doctors(qualification: UpdateQualification, id: int = Path(...,
                                                                                           description=DESCRIPTION_FOR_QUALIFICATION_GET)):
    if qualification.qualification_name is None and qualification.institute_name is None and qualification.year is None:
        raise CustomExceptionHandler(message="empty qualification body",
                                     target='DOC-GET-QUALIFICATIONS', code=status.HTTP_400_BAD_REQUEST,
                                     success=False)
    logger.info("######### GET DOCTOR/QUALIFICATION API CALLED ############")
    check_response = await check_if_qualification_exist(id=id)
    if check_response is None:
        raise CustomExceptionHandler(message="Unable to fetch the given qualification id",
                                     target='DOC-GET-QUALIFICATIONS', code=status.HTTP_400_BAD_REQUEST, success=False)
    logger.info("##### GIVEN ID IS VALID ########")
    query_for_update = "UPDATE qualifications SET "
    values_map = {}
    for key in qualification:
        if not key[1]:
            continue
        values_map[key[0]] = key[1]
        query_for_update = query_for_update + key[0] + "".join("=:") + key[0] + ","
    query_for_update = query_for_update.rstrip(",")
    query_for_update = query_for_update + WHERE_ID_QUALIFICATIONS
    values_map["id"] = id
    try:
        await update_qualifications(query=query_for_update, values_map=values_map)
        return {"message": "Updated id successfully", "code": status.HTTP_200_OK, "success": True}
    except Exception as e:
        raise CustomExceptionHandler(message="Unable To Update In Qualification Table {}".format(e),
                                     target='DOC-GET-QUALIFICATIONS',
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False)
