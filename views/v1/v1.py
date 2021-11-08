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
    if request.query_params is None or request.query_params["value"] is None:
        raise CustomExceptionHandler(message="Please provide username or mail",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="CHECK-REGISTRATION",
                                     success=True
                                     )
    params = request.query_params
    find_user = await find_exist_username_email(params["value"])
    if find_user is not None:
        raise CustomExceptionHandler(message="User is already registered with username or mail",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="CHECK-REGISTRATION",
                                     success=False
                                     )
    return {"message": "new user", "code": status.HTTP_200_OK, "success": True}


@app_v1.post("/doctors/register", status_code=status.HTTP_201_CREATED,
             tags=["DOCTORS/GENERAL"], description="Post call for adding doctors in database")
async def register_user(user: Doctor):
    global object_map
    logger.info("##### REGISTRATION PROCESS STARTED FOR THE USER {} #########".format(user.full_name))
    # check if doctor exist or not
    find_user_by_mail_object = CheckUserByMail(mail=user.mail, target="doctor/registration")
    await find_user_by_mail_object.find_user_by_email()
    if user.phone_number is None:
        logger.error("##### PHONE NUMBER FIELD NOT PROVIDED ##### ")
        raise CustomExceptionHandler(message="Please provide your phone number",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="DOCTOR/REGISTRATION",
                                     success=False
                                     )
    logger.info("#### USER PHONE NUMBER IS NOT NONE ######")
    pattern = re.compile(PHONE_REGEX)
    if not pattern.match(user.phone_number):
        logger.error("##### PHONE NUMBER PATTERN DOESN'T MATCHES PROVIDED ##### ")
        raise CustomExceptionHandler(message="Phone number is not correct",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="DOCTOR/REGISTRATION",
                                     success=False
                                     )
    phone_result_obj = await find_exist_user_phone(phone_number=user.phone_number)
    if phone_result_obj is not None:
        raise CustomExceptionHandler(message="Provided Phone number already exist",
                                     code=status.HTTP_409_CONFLICT,
                                     target="doctor/registration",
                                     success=False
                                     )
    is_array_unique = find_unique_element(specialisation_array=user.specialisation,
                                          languages_array=user.languages)
    if not is_array_unique:
        raise CustomExceptionHandler(message="Something went wrong on our side, Please try again later.",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="doctor/registration,Duplicate Entry in specialisation and languages",
                                     success=False
                                     )

    user.mail = string_to_lower(string_value=user.mail)
    user.experience = string_concatenation_with_years(string_value=user.experience)

    """ TO-DO -> FOR NOW, RANDOMLY GENERATING THE DOCTOR/THERAPIST PASSWORD"""
    user.password = str(random_with_N_digits(n=5))
    user.password = hash_password(password=user.password)
    logger.info("#### RANDOMLY GENERATED USER PASSWORD ##### ")
    slug_object = get_part_of_string(input_string=user.full_name, character="space").lower()
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
        raise CustomExceptionHandler(message="Something went wrong,unable to register you",
                                     target="DOCTOR-REGISTER",
                                     success=False,
                                     code=status.HTTP_400_BAD_REQUEST)


@app_v1.post("/doctors/login", tags=["DOCTORS/GENERAL"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # check if user exist or not
    logger.info("###### LOGGING IN THROUGH MAIL ###### ")
    form_data.username = form_data.username.lower()
    result = await find_exist_username_email(check=form_data.username)
    if not result:
        raise CustomExceptionHandler(message="Something went wrong,user not found.",
                                     code=status.HTTP_404_NOT_FOUND,
                                     target="DOCTORS/LOGIN",
                                     success=False
                                     )
    verify_pass = verify_password(plain_password=form_data.password, hashed_passwrd=result["password"])
    if not verify_pass:
        logger.error("##### Incorrect username or password ######## ")
        raise CustomExceptionHandler(message="Please check your password",
                                     code=status.HTTP_404_NOT_FOUND,
                                     target="DOCTORS/LOGIN",
                                     success=False
                                     )
    # create token
    access_token_expires = jwt_utils.timedelta(minutes=JWT_EXPIRATION_TIME)
    access_token = await jwt_utils.create_access_token(
        data={"sub": form_data.username},
        expire_delta=access_token_expires
    )
    if not access_token:
        raise CustomExceptionHandler(message="Cannot able to create token", success=False,
                                     code=status.HTTP_400_BAD_REQUEST, target="CREATE-DOCTOR")
    else:
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "success": True,
            "details": {
                "id":result["id"],
                "fullname": result["full_name"],
                "message": "user logged in successfully",
                "code": status.HTTP_200_OK
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
        raise CustomExceptionHandler(message="Something went wrong,please try reseting your password later",
                                     success=False,
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="FORGOT-PASSWORD(PATH PARAMETER DOESN'T EXIST)")

    # create reset code and save into database
    reset_code = str(uuid.uuid1())
    try:
        await create_reset_code(request.mail, reset_code)
        background_tasks.add_task(send_email, to_email=request.mail, subject='Reset Password', reset_code=reset_code)
        logger.info("#### SENDING RESET PASSWORD MESSAGE ON THE MAIL {} ########".format(request.mail))
        return {"code": 200, "message": "Email has been sent with instructions to reset password", "success": True}
    except Exception as e:
        logger.error("####### SOMETHING WENT WRONG IN FORGOT PASSWORD MAIL IN USER {} #########".format(e))
        raise CustomExceptionHandler(message="We Regret,Something went wrong in sending mail",
                                     success=False,
                                     code=status.HTTP_409_CONFLICT, target="FORGOT-PASSWORD")
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
        raise CustomExceptionHandler(message="Sorry, password didn't match",
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
            "status": status.HTTP_200_OK,
            "message": "Password has been reset successfully.",
            "success": True
        }
    except Exception as e:
        logger.error("######## EXCEPTION OCCURED IN RESET PASSWORD METHOD {} ###### ".format(e))
    finally:
        logger.info("###### RESET PASSWORD METHOD COMPLETED ######### ")


@app_v1.post("/doctors/images-upload", tags=["DOCTORS/GENERAL"])
async def uploading_image(file: bytes = File(...)):
    logger.info("######## UPLOADING IMAGE FOR THE DOCTOR/THERAPIST ############")
    image_secure_url = cloudinary.uploader.upload(file)
    if not image_secure_url:
        raise CustomExceptionHandler(message="Error in uploading the image",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="IMAGE-UPLOAD", success=False
                                     )
    return {
        "status": status.HTTP_201_CREATED,
        "message": "Image uploaded successfully",
        "url": image_secure_url.get("secure_url"),
        "success": True
    }


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
    consultation_charges = {"chat": doc_or_therapist_results["chat"], "audio": doc_or_therapist_results["audio"],
                            "video": doc_or_therapist_results["video"]}
    doc_or_therapist_results.pop("chat")
    doc_or_therapist_results.pop("audio")
    doc_or_therapist_results.pop("video")
    try:
        logger.info("####### FETCHING DOCTOR INFORMAION FROM THE SLUG ###########")
        doc_or_therapist_information = {
            "languages": await get_language_doctor(id=doc_or_therapist_results["id"]),
            "qualification": await get_doc_qualifications(id=doc_or_therapist_results["id"]),
            "specialisation": await get_specialisation_of_doctor(doctor_id=doc_or_therapist_results["id"]),
            "consultation_charges": consultation_charges
        }
    except Exception as WHY:
        logger.error("####### EXCEPTION IN GETTING DOCTOR DETAILS IS {} ###########".format(WHY))
        raise CustomExceptionHandler(message="Something went wrong,unable to find the results",
                                     target="GET DOCTOR INFORMATION BY SLUG",
                                     code=status.HTTP_400_BAD_REQUEST, success=False)
    else:
        logger.info("##### GETTING FINAL DOCTOR_RESULT INFORMATION MAP ##########")
        doc_or_therapist_results.update(doc_or_therapist_information)
        return doc_or_therapist_results
