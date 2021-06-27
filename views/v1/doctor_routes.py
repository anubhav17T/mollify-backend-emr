from fastapi import status, APIRouter, HTTPException, Depends, Path
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_language_function import get_language_doctor
from utils.db_functions.db_qualifications_function import get_doc_qualifications
from utils.db_functions.db_specialisation_function import update_doctor_status, get_specialisation_of_doctor, \
    get_first_specialisation_of_doctor
from utils.db_functions.raw_queries import WHERE_ID_DOCTORS, QUERY_FOR_UPDATE_DOCTORS_INFORMATION
from utils.helper_function.string_character_finder import get_part_of_string, specific_string
from utils.security.security import verify_password, hash_password
from models.doctor import Doctor, ChangePassword, ChannelName, DoctorStatus, DoctorUpdateInformation
from utils.jwt_utils.jwt_utils import get_current_user, get_token_user
from utils.logger.logger import logger
from conferencing.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee, Role_Publisher
import time
from constants import const
from utils.random_generator.random_digits import random_with_N_digits
from utils.db_functions.db_functions import find_exist_user, get_all_doctor, specific_results_doctor, \
    find_slug_therapist
from utils.db_functions.doctor_crud import change_password_user, save_black_list_token, update_doctor_information
from utils.utils_classes.classes_for_checks import CheckUserExistence, DoctorByName

expireTimeInSeconds = 3600 * 3600
currentTimestamp = int(time.time())
privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

doctor_routes = APIRouter()


@doctor_routes.post("/doctors/video-conferencing", tags=['DOCTORS/RESTRICTED'])
async def videoConferencing(request: ChannelName, current_user: Doctor = Depends(get_current_user)):
    try:
        uid = random_with_N_digits(n=7)
        token = RtcTokenBuilder.buildTokenWithUid(appId=const.APPLICATION_ID,
                                                  appCertificate=const.APPLICATION_CERTIFICATE,
                                                  channelName=str(request.channel_name),
                                                  role=Role_Publisher,
                                                  uid=uid,
                                                  privilegeExpiredTs=privilegeExpiredTs)
        return {"token": token,
                "success": True,
                "channel_name": request.channel_name,
                "uid": uid,
                "Username": current_user.username,
                "mail": current_user.mail,
                "code": 200
                }
    except Exception as e:
        logger.error("#### ERROR IS {} ".format(e))
        return {
            "success": False,
            "Username": current_user.username,
            "mail": current_user.mail
        }


@doctor_routes.get("/doctors/profile/", tags=['DOCTORS/RESTRICTED'])
async def get_user_profile(current_user: Doctor = Depends(get_current_user)):
    try:
        result_db = {"mail": current_user.mail, "full_name": current_user.full_name,
                     "phone_number": current_user.phone_number}
    except Exception as e:
        logger.error("#### ERROR IN GET USER PROFILE ROUTE {} ##### ".format(e))
        return False
    else:
        return result_db
    finally:
        logger.info("###### GET DOCTOR PROFILE METHOD FINISHED #########")


@doctor_routes.patch("/doctors/change-password", tags=['DOCTORS/RESTRICTED'])
async def change_password(change_password_object: ChangePassword, current_user: Doctor = Depends(get_current_user)):
    # check is user exist
    try:
        result = await find_exist_user(mail=current_user.mail)
        if not result:
            logger.error("#### USER NOT REGISTERED #####")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor/Therapist already registered.")
        # Verify current password
        user = Doctor(**result)
        valid = verify_password(change_password_object.current_password, user.password)
        if not valid:
            print("### PASSWORD DIDN'T MATCH ####")
            return {"message": "Current password is not a match", "code": 409}

        # Check new password and confirm password
        if change_password_object.new_password == change_password_object.confirm_password:
            # Change Password
            change_password_object.new_password = hash_password(change_password_object.new_password)
            await change_password_user(change_password_object, current_user)
            return {
                "status_code": status.HTTP_200_OK,
                "detail": "Password has been changed successfully"
            }
        else:
            logger.error("#### NEW PASSWORD AND CONFIRM PASSWORD DIDN'T MATCHED ####")
            return {
                "status_code": status.HTTP_409_CONFLICT,
                "detail": "New and confirm password didn't match"
            }

    except Exception as e:
        logger.error("#### SOMETHING WENT WRONG IN CHANGE_PASSWORD FUNCTION IN USER_ROUTES {} ######".format(e))
    finally:
        logger.info("##### CHANGE PASSWORD METHOD OVER ##### ")


@doctor_routes.get("/doctors/logout", tags=['DOCTORS/RESTRICTED'])
async def logout(token: str = Depends(get_token_user), current_user: Doctor = Depends(get_current_user)):
    # Save token of user to table blacklist
    await save_black_list_token(token, current_user)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "User logout successfully"
    }


@doctor_routes.get("/doctors", tags=["DOCTORS/CRUD"])
async def get_all_doctors():
    logger.info("#### GET ALL DOCTORS ####")
    return await get_all_doctor()


@doctor_routes.get("/doctors/{id}", tags=["DOCTORS/CRUD"], description="GET DOCTOR BY ID")
async def get_specific_doctor_by_id(id: int):
    logger.info("##### GET DOCTOR BY SPECIFIC ID FUNCTION CALLED #####")
    response = CheckUserExistence(_id=id, target="DOCTORS-CRUD-GET-SEPECIFIC-DOCTOR")
    user_info = await response.check_if_user_id_exist()
    if user_info is None:
        raise CustomExceptionHandler(message="Unable to fetch the results",
                                     target="GET DOCTOR BY ID",
                                     code=status.HTTP_400_BAD_REQUEST, success=False)
    logger.info("###### FETCHING INFORMATION OF DOCTOR ###############")
    doc_or_therapist_results = await specific_results_doctor(id=id)
    doc_or_therapist_results = dict(doc_or_therapist_results)
    try:
        logger.info("#### GOING TO FIND DOCTORS LANGUAGES,QUALIFICATIONS AND SPECIALISATION ###########")
        doc_or_therapist_information = {
            "languages": await get_language_doctor(id=id),
            "qualification": await get_doc_qualifications(id=id),
            "specialisation": await get_specialisation_of_doctor(doctor_id=id)
        }
    except Exception as WHY:
        logger.error("####### EXCEPTION IN GETTING USER DETAILS IS {} ###########".format(WHY))
        raise CustomExceptionHandler(message="Unable to fetch the results",
                                     target="GET DOCTOR INFORMATION BY ID",
                                     code=status.HTTP_400_BAD_REQUEST, success=False)
    else:
        logger.info("######## UPDATING FINAL DOCTOR_RESULT MAP ############")
        doc_or_therapist_results.update(doc_or_therapist_information)
        return doc_or_therapist_results


@doctor_routes.patch("/doctors/status/{id}", tags=["DOCTORS/CRUD"], description="Patch call for doctor status")
async def update_status(doctor: DoctorStatus, id: int = Path(..., description="Should be passed as integer")):
    if doctor.is_active is None and doctor.is_online is None:
        raise CustomExceptionHandler(message="No values is passed in request body",
                                     target="DOCTORS-STATUS-PATCH",
                                     code=status.HTTP_404_NOT_FOUND,
                                     success=False)
    logger.info("####### CHECKING THE ID OF THE DOCTOR ########")
    response = CheckUserExistence(_id=id, target="DOCTORS-CRUD-PATCH-DOCTOR-STATUS")
    await response.check_if_user_id_exist()
    logger.info("######## USER EXIST ###########")
    query_for_update = "UPDATE doctors SET "
    values_map = {}
    for key in doctor:
        if key[1] is None:
            continue
        values_map[key[0]] = key[1]
        query_for_update = query_for_update + key[0] + "".join("=:") + key[0] + ","
    query_for_update = query_for_update.rstrip(",")
    query_for_update = query_for_update + WHERE_ID_DOCTORS
    values_map["id"] = id
    check_response = await update_doctor_status(query=query_for_update, values=values_map)
    if not check_response:
        raise CustomExceptionHandler(message="cannot able to update in doctor status",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False,
                                     target="STATUS UPDATE")
    else:
        return {"message": "successfully updated the status",
                "success": True,
                "code": status.HTTP_201_CREATED}


@doctor_routes.get("/doctors/search/{name}", tags=['DOCTORS/CRUD'])
async def find_doctor_by_name(name: str = Path(None, description="NAME OF DOCTOR TO GET THE RESULT")):
    logger.info("##### SEARCH DOCTOR BY NAME METHOD IS CALLED #######")
    if not name:
        return await get_all_doctor()
    logger.info("#### NAME OF THE DOCTOR IS {}".format(name))
    result = DoctorByName(name=name, target='FIND DOCTOR BY NAME')
    return await result.find_doctor_by_name()


global slug_object


@doctor_routes.patch("/doctors/{id}", tags=['DOCTORS/CRUD'], description="Patch call for doctor status")
async def update_doctor_details(doctor_update: DoctorUpdateInformation, id: int):
    global slug_object
    logger.info("####### UPDATE DOCTOR DETAILS API CALLED #############")
    if id is not None:
        logger.info("####### CHECKING THE ID OF THE DOCTOR ########")
        response = CheckUserExistence(_id=id, target="DOCTORS-CRUD-PATCH-DOCTOR-STATUS")
        await response.check_if_user_id_exist()
        logger.info("######## USER EXIST IN THE DATABASE ###########")

    # todo check for username and add functionality of name change and slug
    query_for_update = QUERY_FOR_UPDATE_DOCTORS_INFORMATION
    values_map = {}
    for key in doctor_update:
        if key[1] is None:
            continue
        values_map[key[0]] = key[1]
        query_for_update = query_for_update + key[0] + "".join("=:") + key[0] + ","
    query_for_update = query_for_update.rstrip(",")
    query_for_update = query_for_update + WHERE_ID_DOCTORS
    values_map["id"] = id

    query_for_qualification_update = ""
    if doctor_update.qualification is not None:
        for update in doctor_update.qualification:
            if update.qualification_id is not None:
                pass
            else:
                pass


    if doctor_update.full_name is not None:
        slug_object = get_part_of_string(input_string=doctor_update.full_name, character="space")
        find_first_specialisation_name = await get_first_specialisation_of_doctor(doctor_id=id)
        if find_first_specialisation_name is None:
            raise CustomExceptionHandler(
                message="cannot able to find the specialisation for the doctor having id {}".format(str(id)),
                code=status.HTTP_400_BAD_REQUEST,
                success=False,
                target="STATUS UPDATE")
        speciality = dict(find_first_specialisation_name)
        slug_object = slug_object + "-" + str(speciality["name"]).lower()
        result_slug = await find_slug_therapist(slug=slug_object)
        if result_slug is not None:
            logger.info(
                "###### NAME WITH SAME SLUG NAME IS ALREADY THERE THEREFORE ADDING SOME IDENTFIER ##### ")
            slug_object = slug_object + "-" + str(specific_string(length=4)).lower()
        check_response = await update_doctor_information(doctor_update=doctor_update, doctor_id=id,
                                                         query_for_update=query_for_update,
                                                         update_value_map=values_map,
                                                         slug_object=slug_object)

    else:
        check_response = await update_doctor_information(doctor_update=doctor_update,
                                                         doctor_id=id,
                                                         query_for_update=query_for_update,
                                                         update_value_map=values_map)

    if not check_response:
        raise CustomExceptionHandler(message="cannot able to update in doctor details",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     success=False,
                                     target="STATUS UPDATE")
    else:
        return {"message": "Successfully updated the status",
                "success": True,
                "code": status.HTTP_201_CREATED}
