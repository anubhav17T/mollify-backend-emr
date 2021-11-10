from fastapi import status, APIRouter, Depends
from models.doctor import Doctor
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.helper_function.string_helpers import check_length
from utils.jwt_utils.jwt_utils import get_current_user
from utils.logger.logger import logger
from utils.db_functions.raw_queries import (QUERY_FOR_FEEDBACK_UPDATE,
                                            WHERE_ID_FEEDBACKS)
from models.feedback import (Feedback,
                             FeedbackUpdate)
from utils.utils_classes.classes_for_checks import (CheckUserExistence,
                                                    ConsultationValidity)
from utils.db_functions.db_feedback_function import (save_feedback,
                                                     get_all_feedbacks,
                                                     find_if_feedback_exist, update_feedback)

doctor_feedback = APIRouter()


# @doctor_feedback.get("/doctors/feedback/", tags=["DOCTORS/FEEDBACKS"], description="GET CALL FOR FEEDBACKS")
# async def get_feedbacks_doctor(doctor_id: int):
#     logger.info("##### GET SPECIFIC FEEDBACK METHOD CALLED ########")
#     response = CheckUserExistence(_id=doctor_id, target="SAVE-FEEDBACK")
#     await response.check_if_user_id_exist()
#     # todo:change it to internal api call because using same database
#     logger.info("###### GETTING ALL THE FEEDBACKS FOR SPECIFIC DOCTOR ID ############")
#     response = await get_all_feedbacks(doctor_id=doctor_id)
#     if not response:
#         return {"message": "Sorry, No Feedbacks Found",
#                 "code": status.HTTP_200_OK,
#                 "success": True,
#                 "data": []}
#     return {"message": "Here is your feedbacks",
#             "code": status.HTTP_200_OK,
#             "success": True, "data": response}


@doctor_feedback.get("/doctors/feedback/", tags=["DOCTORS/RESTRICTED"], description="GET CALL FOR FEEDBACKS")
async def get_feedbacks_doctor(current_user: Doctor = Depends(get_current_user)):
    logger.info("##### GET SPECIFIC FEEDBACK METHOD CALLED ########")
    # todo:change it to internal api call because using same database
    logger.info("###### GETTING ALL THE FEEDBACKS FOR SPECIFIC DOCTOR ID ############")
    response = await get_all_feedbacks(doctor_id=current_user["id"])
    if not response:
        return {"message": "Sorry, No Feedbacks Found",
                "code": status.HTTP_200_OK,
                "success": True,
                "data": []}
    return {"message": "Here is your feedbacks",
            "code": status.HTTP_200_OK,
            "success": True,
            "data": response}
