from fastapi import status, APIRouter, HTTPException, Depends, UploadFile, File
from utils.db_functions.db_feedback_function import save_feedback, get_feedbacks, get_specific_doctor_feedback, \
    get_all_feedbacks
from utils.logger.logger import logger
from models.feedback import Feedback
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.utils_classes.classes_for_checks import CheckUserExistence

doctor_feedback = APIRouter()


@doctor_feedback.post("/doctors/feedbacks", tags=["DOCTORS/FEEDBACKS"], description="POST CALL FOR DOCTOR FEEDBACK")
async def create_feedback(feedback: Feedback):
    logger.info("##### CREATE FEEDBACK METHOD CALLED ########")
    # Check to see if doctor exist by that id
    response = CheckUserExistence(_id=feedback.doctor_id, target="SAVE-FEEDBACK")
    await response.check_if_user_id_exist()

    save_feedback_resp_id = await save_feedback(feedback)
    if not save_feedback_resp_id:
        raise CustomExceptionHandler(message="unable to insert the data in feedback table",
                                     code=status.HTTP_409_CONFLICT,
                                     success=False, target="SAVE-FEEDBACK")
    return {"message": "Thank you for your feedback", "code": status.HTTP_201_CREATED, "success": True}


# cache this results later
@doctor_feedback.get("/doctors/feedback/{id}", tags=["DOCTORS/FEEDBACKS"], description="GET CALL FOR FEEDBACKS")
async def get_feedbacks_doctor(id: int):
    logger.info("##### GET SPECIFIC FEEDBACK METHOD CALLED ########")
    response = CheckUserExistence(_id=id, target="SAVE-FEEDBACK")
    await response.check_if_user_id_exist()
    # get names of a patient id and implement joins using equi join
    logger.info("###### GETTING ALL THE FEEDBACKS FOR SPECIFIC DOCTOR ID ############")
    response = await get_all_feedbacks(doctor_id=id)
    if not response:
        raise CustomExceptionHandler(message="No Feedbacks For Specific Doctor", code=status.HTTP_400_BAD_REQUEST,
                                     success=False, target="GET-SPECIFIC-FEEDBACK")
    return response
