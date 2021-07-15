from fastapi import status, APIRouter
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.helper_function.string_helpers import check_length
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


@doctor_feedback.post("/doctors/feedbacks", tags=["DOCTORS/FEEDBACKS"], description="POST CALL FOR DOCTOR FEEDBACK")
async def create_feedback(feedback: Feedback):
    logger.info("##### CREATE FEEDBACK METHOD CALLED ########")
    string_length = check_length(string=feedback.review)
    if not string_length:
        logger.error("####### STRING LENGTH DOESNT NOT MATCHES #############")
        raise CustomExceptionHandler(message="Either review is greater than 500 words or less than 40 words",
                                     code=status.HTTP_409_CONFLICT,
                                     success=False, target="SAVE-FEEDBACK")

    response = ConsultationValidity(consultation_id=feedback.consultation_id,
                                    doctor_id=feedback.doctor_id,
                                    patient_id=feedback.patient_id)
    await response.consultation_utils()
    await response.review_exist()
    save_feedback_resp_id = await save_feedback(feedback)
    if not save_feedback_resp_id:
        raise CustomExceptionHandler(message="unable to insert the data in feedback table",
                                     code=status.HTTP_409_CONFLICT,
                                     success=False, target="SAVE-FEEDBACK")
    return {"message": "Thank you for your feedback", "code": status.HTTP_201_CREATED, "success": True}


@doctor_feedback.get("/doctors/feedback/{doctor_id}", tags=["DOCTORS/FEEDBACKS"], description="GET CALL FOR FEEDBACKS")
async def get_feedbacks_doctor(doctor_id: int):
    logger.info("##### GET SPECIFIC FEEDBACK METHOD CALLED ########")
    response = CheckUserExistence(_id=doctor_id, target="SAVE-FEEDBACK")
    await response.check_if_user_id_exist()
    # todo:change it to internal api call because using same database
    logger.info("###### GETTING ALL THE FEEDBACKS FOR SPECIFIC DOCTOR ID ############")
    response = await get_all_feedbacks(doctor_id=doctor_id)
    if not response:
        raise CustomExceptionHandler(message="No Feedbacks For Specific Doctor", code=status.HTTP_400_BAD_REQUEST,
                                     success=False, target="GET-SPECIFIC-FEEDBACK")
    return response


@doctor_feedback.put("/doctors/feedback/{feedback_id}", tags=["DOCTORS/FEEDBACKS"],
                     description="UPDATE CALL FOR DOCTOR FEEDBACKS")
async def update_doctor_feedbacks(feedback_id: int, feedback_update: FeedbackUpdate):
    logger.info("########## GET SPECIFIC FEEDBACK METHOD CALLED ########")
    response = await find_if_feedback_exist(feedback_id=feedback_id)
    if response is None:
        raise CustomExceptionHandler(message="No Feedback Exist", code=status.HTTP_400_BAD_REQUEST,
                                     success=False, target="GET-SPECIFIC-FEEDBACK")
    logger.info("####### FEEDBACK ID FOUND, PROCEEDING FURTHER ################ ")
    feedback_update_query = QUERY_FOR_FEEDBACK_UPDATE
    values_map = {"id": feedback_id}
    for values in feedback_update:
        if values[1] is None:
            continue
        feedback_update_query = feedback_update_query + values[0] + "".join("=:") + values[0] + ","
        values_map[values[0]] = values[1]
    feedback_update_query = feedback_update_query.rstrip(",") + WHERE_ID_FEEDBACKS
    response = await update_feedback(query=feedback_update_query, values_map=values_map)
    if not response:
        raise CustomExceptionHandler(message="Sorry, cannot able to update your feedback",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False, target="GET-SPECIFIC-FEEDBACK")
    else:
        return {"message": "Your feedback is updated,thanks !!", "code": status.HTTP_200_OK, "success": True}
