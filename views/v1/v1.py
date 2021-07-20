from fastapi import Request, BackgroundTasks
import re
from fastapi import status, APIRouter, HTTPException, Depends
from mail.sendgrid_services.sendgrid_email_configuration import send_email
from utils.db_functions.db_language_function import get_language_doctor
from utils.db_functions.db_qualifications_function import get_doc_qualifications
from utils.db_functions.db_specialisation_function import get_specialisation_of_doctor
from utils.helper_function.string_helpers import string_to_lower, string_concatenation_with_years
from utils.helper_function.unique_characters_array import find_unique_element
from utils.logger.logger import logger
from models.doctor import Doctor, ForgotPassword, ResetPassword
from utils.random_generator.random_digits import random_with_N_digits
from utils.security.security import hash_password, verify_password
from constants.const import PHONE_REGEX, ADDING_YEARS
from utils.jwt_utils import jwt_utils
from constants.const import JWT_EXPIRATION_TIME
from fastapi.security import OAuth2PasswordRequestForm
import uuid
import cloudinary
from fastapi import File
from cloudinary import uploader
from fastapi import Path
from constants.const import CLOUD_NAME, API_KEY, API_SECRET
from utils.helper_function.string_character_finder import get_part_of_string, specific_string
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.utils_classes.classes_for_checks import CheckUserByMail
from utils.db_functions.db_functions import (
    find_exist_username_email,
    find_exist_user_phone,
    find_slug_therapist, \
    create_reset_code,
    check_reset_password_token, \
    reset_password_user,
    disable_reset_code,
    find_specialisation,
    find_doctor_information, \
    register_user_combined
)

global object_map

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

app_v1 = APIRouter()


@app_v1.get("/doctors/check-registration/", response_model_exclude_unset=True, tags=["DOCTORS/GENERAL"])
async def check_availability(request: Request):
    logger.info("####### CHECK REGISTRATION OF THE DOCTOR/THERAPIST ###### ")
    try:
        if request.query_params is None:
            return {"error": {"code": 400,
                              "message": "value required for username or email",
                              "target": "check-registration",
                              "success": True}}

        params = request.query_params
        if params["value"] is None:
            return {"error": {"code": 400,
                              "message": "value required for username or email",
                              "target": "check-registration",
                              "success": True}}
        else:
            find_exist_asset = await find_exist_username_email(params["value"])
            if find_exist_asset is not None:
                return {"error": {"code": status.HTTP_409_CONFLICT,
                                  "message": "user has already registered with  username or mail",
                                  "success": True}
                        }
            else:
                return {"message": "welcome!! new user", "code": status.HTTP_200_OK, "success": False}
    except Exception as e:
        logger.error("Exception occurred in user check function {}".format(e))
    finally:
        logger.info("######## CHECK DOCTOR-REGISTRATION METHOD FINISHED ########")


@app_v1.post("/doctors/register", status_code=status.HTTP_201_CREATED,
             tags=["DOCTORS/GENERAL"], description="Post call for adding doctors in database")
async def register_user(user: Doctor):
    global object_map
    user.Config.orm_mode = True
    logger.info("##### REGISTRATION PROCESS STARTED FOR THE USER {} #########".format(user.full_name))
    # check if doctor exist or not
    find_user_by_mail_object = CheckUserByMail(mail=user.mail, target="doctor/registration")
    await find_user_by_mail_object.find_user_by_email()
    if user.phone_number is None:
        logger.error("##### PHONE NUMBER FIELD NOT PROVIDED ##### ")
        raise CustomExceptionHandler(message="Please provide phone number",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="doctor/registration",
                                     success=False
                                     )
    logger.info("#### USER PHONE NUMBER IS NOT NONE ######")
    pattern = re.compile(PHONE_REGEX)
    if not pattern.match(user.phone_number):
        logger.error("##### PHONE NUMBER PATTERN DOESN'T MATCHES PROVIDED ##### ")
        raise CustomExceptionHandler(message="Please provide phone number",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="doctor/registration",
                                     success=False
                                     )
    phone_result_obj = await find_exist_user_phone(phone_number=user.phone_number)
    if phone_result_obj is not None:
        raise CustomExceptionHandler(message="Provided phone number already exist",
                                     code=status.HTTP_409_CONFLICT,
                                     target="doctor/registration",
                                     success=False
                                     )
    is_array_unique = find_unique_element(specialisation_array=user.specialisation,
                                          languages_array=user.languages)
    if not is_array_unique:
        raise CustomExceptionHandler(message="Duplicate Entry in specialisation and languages",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="doctor/registration",
                                     success=False
                                     )

    user.mail = string_to_lower(string_value=user.mail)
    user.experience = string_concatenation_with_years(string_value=user.experience)

    """ TO-DO -> FOR NOW, RANDOMLY GENERATING THE DOCTOR/THERAPIST PASSWORD"""
    user.password = str(random_with_N_digits(n=5))
    user.password = hash_password(password=user.password)
    logger.info("#### RANDOMLY GENERATED USER PASSWORD ##### ")
    slug_object = get_part_of_string(input_string=user.full_name, character="space")
    specialisation_name_object = await find_specialisation(specialisation_value=user.specialisation[0])
    if specialisation_name_object is None:
        return {"error": {"message": "Unable to find the provided specialisation in the database",
                          "code": status.HTTP_404_NOT_FOUND,
                          "success": False,
                          "target": "FIND SPECIFIC-SPECIALISATION"
                          }}
    speciality = dict(specialisation_name_object)
    slug_object = slug_object + "-" + str(speciality["name"]).lower()
    result_slug = await find_slug_therapist(slug=slug_object)
    if result_slug is not None:
        logger.info(
            "###### NAME WITH SAME SLUG NAME IS ALREADY THERE THEREFORE ADDING SOME IDENTFIER ##### ")
        slug_object = slug_object + "-" + str(specific_string(length=4)).lower()
    if user.is_active is None:
        user.is_active = False
    if user.is_online is None:
        user.is_online = False
    success_ = await register_user_combined(doctor=user, slug=slug_object)
    if success_:
        access_token_expires = jwt_utils.timedelta(minutes=JWT_EXPIRATION_TIME)
        access_token = await jwt_utils.create_access_token(
            data={"sub": user.mail},
            expire_delta=access_token_expires
        )
        if not access_token:
            raise HTTPException(status_code=404, detail="Cannot create access token")
        else:
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "success": True,
                "user_info": {
                    "email": user.mail,
                    "fullname": user.full_name,
                    "message": "Doctor/Therapist created successfully",
                    "code": status.HTTP_201_CREATED,
                }
            }
    else:
        raise CustomExceptionHandler(message="UNABLE TO REGISTER THE USER",
                                     target="DOCTOR-REGISTER",
                                     success=False,
                                     code=status.HTTP_400_BAD_REQUEST)


@app_v1.post("/doctors/login", tags=["DOCTORS/GENERAL"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # check if user exist or not
    global result, through_access_token
    logger.info("###### LOGGING IN THROUGH MAIL ###### ")
    form_data.username = form_data.username.lower()
    result = await find_exist_username_email(check=form_data.username)
    if not result:
        return {"status": 404, "message": "User not found", "success": False}
    through_access_token = form_data.username
    # verify password
    user = Doctor(**result)
    verify_pass = verify_password(plain_password=form_data.password, hashed_passwrd=user.password)
    if not verify_pass:
        logger.error("##### Incorrect username or password ######## ")
        return {"status": 400, "message": "Incorrect username or password", "success": False}
    # create token
    access_token_expires = jwt_utils.timedelta(minutes=JWT_EXPIRATION_TIME)
    access_token = await jwt_utils.create_access_token(
        data={"sub": form_data.username},
        expire_delta=access_token_expires
    )
    if not access_token:
        raise CustomExceptionHandler(message="cannot able to create token", success=False,
                                     code=status.HTTP_400_BAD_REQUEST, target="CREATE-DOCTOR")
    else:
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "success": True,
            "user_info": {
                "fullname": user.full_name,
                "message": "user logged in successfully",
                "code": 200
            }
        }


@app_v1.post("/doctors/forgot-password/{through}", tags=["DOCTORS/GENERAL"])
async def forget_password(request: ForgotPassword, background_tasks: BackgroundTasks,
                          through: str = Path(..., title="to check whether user has logged "
                                                         "in through mail/phone")):
    if through == "mail":
        result = await find_exist_username_email(check=request.mail)
        if not result:
            raise CustomExceptionHandler(message="Doctor/Therapist not found",
                                         success=False,
                                         code=status.HTTP_400_BAD_REQUEST, target="FORGOT-PASSWORD")
    elif through == "phone_number":
        result = await find_exist_user_phone(phone_number=request.phone_number)
        if not result:
            raise CustomExceptionHandler(message="Doctor/Therapist not found",
                                         success=False,
                                         code=status.HTTP_400_BAD_REQUEST, target="FORGOT-PASSWORD")
    else:
        logger.error("###### ERROR IN PATH PARAMETER NOT DEFINED ####### ")
        raise CustomExceptionHandler(message="ERROR IN PATH PARAMETER NOT DEFINED",
                                     success=False,
                                     code=status.HTTP_400_BAD_REQUEST, target="FORGOT-PASSWORD")

    # create reset code and save into database
    reset_code = str(uuid.uuid1())
    try:
        await create_reset_code(request.mail, reset_code)
        background_tasks.add_task(send_email, to_email=request.mail, subject='Reset Password', reset_code=reset_code)
        try:
            logger.info("#### SENDING RESET PASSWORD MESSAGE ON THE MAIL {} ########".format(request.mail))
            logger.info("### ALL GOOD #####")
            return {
                "reset_code": reset_code,
                "code": 200,
                "message": "Email has been sent with instructions to reset password",
                "success": True
            }
        except Exception as e:
            logger.error(
                "###### EXCEPTION OCCURRED IN SENDING FORGOT PASSWORD FOR THE MAIL {} WITH EXCEPTION {} ###".format(
                    request.mail, e))
            raise CustomExceptionHandler(message="Error, email not send",
                                         success=False,
                                         code=status.HTTP_409_CONFLICT, target="FORGOT-PASSWORD")
    except Exception as e:
        logger.error("####### SOMETHING WENT WRONG IN FORGOT PASSWORD MAIL IN USER {} #########".format(e))
    finally:
        logger.info("###### FORGOT PASSWORD MAIL FUNCTION OVER ##### ")


@app_v1.post("/doctors/reset-password", tags=["DOCTORS/GENERAL"])
async def reset_password(request: ResetPassword):
    # Check valid reset password token
    reset_token = await check_reset_password_token(request.reset_password_token)
    if not reset_token:
        logger.error("####### RESET PASSWORD TOKEN HAS EXPIRED ######## ")
        raise CustomExceptionHandler(message="Reset password token has expired,please request a new one", success=False,
                                     code=status.HTTP_400_BAD_REQUEST, target="RESET-PASSWORD")

    # Check if both new & confirm password are same
    if request.new_password != request.confirm_password:
        logger.error("###### NEW PASSWORD AND CONFIRM PASSWORD ARE NOT A MATCH ######### ")
        raise CustomExceptionHandler(message="PASSWORD DIDN'T MATCH",
                                     success=False,
                                     code=status.HTTP_409_CONFLICT,
                                     target="RESET-PASSWORD")

    # Reset new password
    forgot_password_object = ForgotPassword(**reset_token)
    new_hashed_password = hash_password(request.new_password)
    await reset_password_user(new_hashed_password, forgot_password_object.mail)
    # Disable reset code (that is already used)
    try:
        await disable_reset_code(request.reset_password_token, forgot_password_object.mail)
        return {
            "status": 200,
            "message": "Password has been reset successfully.",
            "success": True
        }
    except Exception as e:
        logger.error("######## EXCEPTION OCCURED IN RESET PASSWORD METHOD {} ###### ".format(e))
    finally:
        logger.info("###### RESET PASSWORD METHOD COMPLETED ######### ")


@app_v1.put("/doctors/image-upload", tags=["DOCTORS/GENERAL"])
async def uploading_image(file: bytes = File(...)):
    try:
        logger.info("######## UPDATING IMAGE FOR THE DOCTOR/THERAPIST {} ####")
        logger.info("#### USERNAME IS VALID #####")
        result_ = cloudinary.uploader.upload(file)
        url = result_.get("secure_url")
        return {
            "status": status.HTTP_201_CREATED,
            "message": "Image uploaded successfully",
            "url": url,
            "success": True
        }
    except Exception as e:
        logger.error("######## EXCEPTION OCCURED IN IMAGE UPLOAD METHOD {} ###### ".format(e))
        raise CustomExceptionHandler(message="unable to upload the image", code=status.HTTP_400_BAD_REQUEST,
                                     target="IMAGE-UPLOAD", success=False
                                     )
    finally:
        logger.info("####### UPLOADING IMAGE METHOD COMPLETED ######")


@app_v1.get("/doctors/information/{slug}", tags=["DOCTORS/GENERAL"])
async def get_doctor_information(slug: str = Path(...)):
    logger.info("###### GET DOCTOR INFORMATION FUNCTION IS CALLED #######")
    doctor_information = await find_doctor_information(slug=slug)
    if not doctor_information:
        raise CustomExceptionHandler(message="Unable to find the information for the specific slug",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="INFORMATION FROM SLUG", success=False
                                     )
    doc_or_therapist_results = dict(doctor_information)
    try:
        logger.info("####### FETCHING DOCTOR INFORMAION FROM THE SLUG ###########")
        doc_or_therapist_information = {
            "languages": await get_language_doctor(id=doc_or_therapist_results["id"]),
            "qualification": await get_doc_qualifications(id=doc_or_therapist_results["id"]),
            "specialisation": await get_specialisation_of_doctor(doctor_id=doc_or_therapist_results["id"])
        }
    except Exception as WHY:
        logger.error("####### EXCEPTION IN GETTING DOCTOR DETAILS IS {} ###########".format(WHY))
        raise CustomExceptionHandler(message="Unable to fetch the results",
                                     target="GET DOCTOR INFORMATION BY SLUG",
                                     code=status.HTTP_400_BAD_REQUEST, success=False)
    else:
        logger.info("##### GETTING FINAL DOCTOR_RESULT INFORMATION MAP ##########")
        doc_or_therapist_results.update(doc_or_therapist_information)
        return doc_or_therapist_results
