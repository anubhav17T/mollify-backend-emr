from fastapi import APIRouter
from fastapi import Request, Path, Query
from fastapi import status, APIRouter, HTTPException, Depends
from models.languages import LanguagesUpdate
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_functions import get_all_languages, save_languages, find_particular_language
from utils.db_functions.db_language_function import get_language_doctor
from utils.logger.logger import logger
from utils.utils_classes.classes_for_checks import CheckUserExistence

doctor_languages = APIRouter()


@doctor_languages.get("/doctors/languages/", tags=["DOCTORS/LANGUAGES"], description="Get Languages")
async def get_languages():
    logger.info("####### GET LANGUAGES API CALL ############")
    try:
        response_ = await get_all_languages()
        if response_ is None:
            raise CustomExceptionHandler(message="Unable to fetch languages",
                                         target="DOCTORS-LANGUAGES",
                                         success=False,
                                         code=status.HTTP_400_BAD_REQUEST)
        return response_
    except Exception as WHY:
        logger.error("######## UNABLE TO FIND THE DOCTOR LANGUAGES {} #########".format(WHY))
    finally:
        logger.info("####### METHOD FOR FINDING ALL TE")


@doctor_languages.post("/doctors/languages/", tags=["DOCTORS/LANGUAGES"], description="Add/Post Languages")
async def add_languages(languages: LanguagesUpdate):
    logger.info("##### ADD/POST SPECIALISATION API CALLED #######")
    if languages.is_active is None:
        languages.is_active = True
    # CHECK if language already exist or not
    check_response = await find_particular_language(name=languages.name)
    if check_response is not None:
        raise CustomExceptionHandler(message="Unable to save languages because language already exist",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False,
                                     target="SAVE-LANGUAGES"
                                     )
    await save_languages(languages=languages)
    return {"message": "languages added successfully", "code": status.HTTP_201_CREATED, "success": True}


@doctor_languages.get("/doctors/languages/{doctor_id}", tags=["DOCTORS/LANGUAGES"],
                      description="Get Languages of specific doctor")
async def get_doctor_language(doctor_id:int):
    logger.info("##### GET LANGUAGES FOR SPECIFIC DOCTOR API CALL ######")
    response = CheckUserExistence(_id=doctor_id, target="GET[DOCTOR-LANGUAGES]")
    await response.check_if_user_id_exist()
    logger.info("### DOCTOR EXIST #######")
    try:
        return await get_language_doctor(id=doctor_id)
    except Exception as e:
        raise CustomExceptionHandler(message="Unable to get languages for specific doctor because {}".format(e),
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False,
                                     target="GET-SPECIFIC-LANGUAGES"
                                     )
    finally:
        logger.info("###### GET SPECIFIC DOCTOR LANGUAGE METHOD IS OVER ##########")


@doctor_languages.patch("/doctors/languages", tags=["DOCTORS/LANGUAGES"], description="Patch for languages")
async def edit_doctor_language():
    logger.info("###### PATCH METHOD FOR DOCTOR LANGUAGE ########")
    pass






# @app_v1.get("/doctors/languages/", tags=["DOCTORS/LANGUAGES"], description="Get languages")
# async def get_languages(active_state: str = Query(None, title="Query parameter for search",
#                                                   description="Provide values in type(string)= true/false/getAll")):
#     logger.info("###### GET SPECIALISATION ######## ")
#     try:
#         if active_state == "true" or active_state is None:
#             return await get_true_languages()
#         elif active_state == "false":
#             return await get_false_languages()
#         elif active_state == "getAll":
#             return await get_all_languages()
#         else:
#             return {"error": {"message": "no parameter found", "code": status.HTTP_404_NOT_FOUND, "success": False}}
#     except Exception as e:
#         logger.error("### ERROR IN DOCTORS LANGUAGES {} ####".format(e))
#         return {"error":
#                     {"message": "no parameter found",
#                      "code": status.HTTP_404_NOT_FOUND,
#                      "success": False}}
#     finally:
#         logger.info("######## GET LANGUAGES FUNCTION OVER ##########")
#
#
# @app_v1.patch("/doctors/languages/{language_id}", tags=["DOCTORS/LANGUAGES"],
#               description="Update languages")
# async def update_language_name(language: Languages,
#                                language_id: int = Path(..., description="Should be passed as integer")):
#     if language_id is None:
#         return {"error": {"message": "please provide id",
#                           "code": status.HTTP_400_BAD_REQUEST,
#                           "success": False
#                           }
#                 }
#     response = await check_if_language_id_exist(id=language_id)
#     if response is None:
#         raise CustomExceptionHandler(message="no id found", code=status.HTTP_400_BAD_REQUEST, success=False,
#                                      target='UPDATE LANGUAGE NAME')
#     check_resp = await update_language(id=language_id, name=language.name)
#     if not check_resp:
#         raise CustomExceptionHandler(message="cannot able to insert in the languages", code=status.HTTP_400_BAD_REQUEST,
#                                      success=False,
#                                      target='UPDATE LANGUAGE NAME')
#     else:
#         return {"message": "Successfully Updated the language", "success": True, "code": status.HTTP_201_CREATED}
