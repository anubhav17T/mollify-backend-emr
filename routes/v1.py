from fastapi import Request
import re
from fastapi import status, APIRouter, HTTPException, Depends
from utils.logger.logger import logger
from utils.db_functions.db_functions import find_exist_username_email, find_exist_user, find_exist_username, \
    find_exist_user_phone, find_slug_therapist, save_doctor, create_reset_code, check_reset_password_token, \
    reset_password_user, disable_reset_code, save_qualification, \
    save_specialisation, get_sepecific_specialisation, get_all_specialisation, save_specialisation_map, get_all_doctor, \
    get_true_specialisation, get_false_specialisation
from models.doctor import Doctor, ForgotPassword, ResetPassword
from models.specialisation import Specialisation
from utils.random_generator.random_digits import random_with_N_digits
from utils.security.security import hash_password, verify_password
from constants.const import PHONE_REGEX
from utils.jwt_utils import jwt_utils
from constants.const import JWT_EXPIRATION_TIME
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uuid
import cloudinary
from fastapi import File
from cloudinary import uploader
from fastapi import Query, Path
from constants.const import CLOUD_NAME, API_KEY, API_SECRET

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

app_v1 = APIRouter()


@app_v1.get("/doctors/", tags=["DOCTORS/CRUD"])
async def get_all_doctors():
    logger.info("#### GET ALL DOCTORS ####")
    return await get_all_doctor()


@app_v1.post("/doctors/specialisations", tags=["DOCTORS/SPECIALISATIONS"], description="Create specialisation")
async def adding_specialisation(specailisation: Specialisation):
    logger.info("###### ADDING SPECIALISATION ######## ")
    try:
        await save_specialisation(specailisation)
        return {"message": "specialisation added successfully", "code": status.HTTP_201_CREATED, "success": True}
    except Exception as e:
        logger.error("###### ERROR IN ADDING SPECIALISATION {} ###########".format(e))
        return {"error": {
            "message": "Unable to save specialisation {}".format(e),
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "target": "SAVE-SPECIALISATION"
        }}
    finally:
        logger.info("#### REGISTER SPECIALISATION FUNCTION OVER #####")


@app_v1.get("/doctors/specialisations", tags=["DOCTORS/SPECIALISATIONS"], description="Get specialisations")
async def get_specialisations(active_state: str = Query(None, title="Query parameter for search",
                                                        description="Provide values in type(string)= true/false/getAll")):
    logger.info("###### GET SPECIALISATION ######## ")
    try:
        if active_state == "true" or active_state is None:
            return await get_true_specialisation()
        elif active_state == "false":
            return await get_false_specialisation()
        elif active_state == "getAll":
            return await get_all_specialisation()
        else:
            return {"error": {"message": "no parameter found", "code": status.HTTP_404_NOT_FOUND, "success": False}}
    except Exception as e:
        logger.error("### ERROR IN DOCTORS SPECIALISATION {} ####".format(e))
        return {"error":
                    {"message": "no parameter found",
                     "code": status.HTTP_404_NOT_FOUND,
                     "success": False}}
    finally:
        logger.info("##### GET SPECIALISATIONS FUNCTION OVER #####")





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


@app_v1.get("/doctors/{mail}", tags=["DOCTORS/CRUD"])
async def get_doctor(mail: str):
    logger.info("#### CALL FOR SPECIFIC DOCTOR ####")
    try:
        result_ = await find_exist_user(mail)
        if result_ is None:
            return {"error": {
                "message": "cannot able to find the doctor/therapist",
                "code": status.HTTP_404_NOT_FOUND,
                "success": False,
                "target": "GET-DOCTOR"
            }}
        else:
            return {"info": result_, "success": True}
    except Exception as e:
        logger.error("### ERROR IN GET SPECIFIC DOCTOR ID IS {} ####".format(e))
        return {"error": {
            "message": "Unable to get doctor information {}".format(e),
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False
        }}


@app_v1.post("/doctors/register", status_code=status.HTTP_201_CREATED,
             tags=["DOCTORS/GENERAL"], description="Post call for addings doctors")
async def register_user(user: Doctor):
    global object_map
    user.Config.orm_mode = True
    logger.info("##### REGISTRATION PROCESS STARTED #########")
    # check if doctor exist or not
    try:
        result = await find_exist_user(mail=user.mail)
        if result is not None:
            logger.error("#### USER ALREADY REGISTERED  WITH MAIL #####")
            return {"error": {"message": "Doctor/Therapist has already registered",
                              "code": status.HTTP_409_CONFLICT,
                              "target": "doctor/registration",
                              "success": False}
                    }

        # result_obj = await find_exist_username(username=user.username)
        # if result_obj is not None:
        #     logger.error("#### USER ALREADY REGISTERED  WITH USERNAME #####")
        #     return {"error": {"message": "Doctor/Therapist has already registered",
        #                       "code": status.HTTP_409_CONFLICT,
        #                       "target": "doctor/registration",
        #                       "success": False}
        #             }
        else:
            if user.phone_number is None:
                logger.error("##### PHONE NUMBER FIELD NOT PROVIDED ##### ")
                return {"error": {"message": "Please provide phone number",
                                  "code": status.HTTP_400_BAD_REQUEST,
                                  "target": "doctor/registration",
                                  "success": False}
                        }
            elif user.phone_number is not None:
                logger.info("###### PHONE NUMBER IS NOT NONE ###########")
                pattern = re.compile(PHONE_REGEX)
                if pattern.match(user.phone_number):
                    logger.info("###### VALID PHONE NUMBER ######### ")
                    phone_result_obj = await find_exist_user_phone(phone_number=user.phone_number)
                    if phone_result_obj is not None:
                        logger.error("####### PHONE IS ALREADY REGISTERED #########")
                        return {"error": {"message": "Your phone number has already been used for registration",
                                          "status": status.HTTP_409_CONFLICT, "target": "doctor/registration[Phone]",
                                          "success": False}}

                    """ TO-DO -> FOR NOW, RANDOMLY GENERATING THE DOCTOR/THERAPIST PASSWORD"""
                    user.password = str(random_with_N_digits(n=5))
                    user.password = hash_password(password=user.password)
                    logger.info("#### RANDOMLY GENERATED USER PASSWORD ##### ")
                    slug_object = user.full_name + "-" + str(random_with_N_digits(n=2))
                    result_slug = await find_slug_therapist(slug=slug_object)
                    if result_slug is not None:
                        logger.info(
                            "###### NAME WITH SAME SLUG NAME IS ALREADY THERE THEREFORE ADDING SOME IDENTFIER ##### ")
                        slug_object = slug_object + "-" + str(random_with_N_digits(n=3))
                        doctor_id = await save_doctor(doctor=user, slug=slug_object)
                        values = []
                        for get_values in user.qualification:
                            qualification_object = {"doctor_id": doctor_id,
                                                    "qualification_name": get_values.qualification_name,
                                                    "institute_name": get_values.institute_name,
                                                    "year": get_values.year
                                                    }
                            values.append(qualification_object)
                        logger.info("####### GOING GOR QUALIFICATION TABLE INSERTION ########## ")
                        await save_qualification(values=values)
                        logger.info(
                            "#####  NEW THERAPIST CREATED SUCCESSFULLY WITH NAME {} #########".format(user.full_name))
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
                                "user_info": {
                                    "email": user.mail,
                                    "fullname": user.full_name,
                                    "message": "Doctor/Therapist created successfully",
                                    "code": status.HTTP_201_CREATED,
                                    "success": True
                                }
                            }
                    else:
                        logger.info("###### NO MATCHING SLUG WAS FOUND ######### ")
                        doctor_id = await save_doctor(doctor=user, slug=slug_object)
                        map_object = []
                        for get_index in user.specialisation:
                            object_map = {"doctor_id": doctor_id,
                                          "specialisation_id": get_index
                                          }
                            map_object.append(object_map)
                        await save_specialisation_map(map=map_object)
                        values = []
                        for get_values in user.qualification:
                            qualification_object = {"doctor_id": doctor_id,
                                                    "qualification_name": get_values.qualification_name,
                                                    "institute_name": get_values.institute_name,
                                                    "year": get_values.year
                                                    }
                            values.append(qualification_object)
                        logger.info("###### GOING FOR SAVE QUALIFICATION TABLE ######### ")
                        await save_qualification(values=values)
                        logger.info("#####  NEW THERAPIST CREATED SUCCESSFULLY WITH NAME #########")
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
                                "user_info": {
                                    "email": user.mail,
                                    "fullname": user.full_name,
                                    "message": "Doctor/Therapist created successfully",
                                    "code": 200,
                                    "success": True
                                }
                            }
                else:
                    return {"message": "invalid phone number", "status": status.HTTP_409_CONFLICT, "success": False}
    except Exception as e:
        logger.error("###### ERROR IN REGISTRATION FOR DOCTOR/THERAPIST EXCEPTION {} ###########".format(e))
        return {"error": {"message": "unable to register doctor information {}".format(e),
                          "code": status.HTTP_400_BAD_REQUEST,
                          "success": False,
                          "target": "Register_Main"
                          }}
    finally:
        logger.info("#### REGISTER DOCTOR/THEAPIST FUNCTION OVER #####")


@app_v1.post("/doctors/login", tags=["DOCTORS/GENERAL"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # check if user exist or not
    global result, through_access_token
    logger.info("###### LOGGING IN THROUGH MAIL ###### ")
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
        return {"status": 400, "message": "cannot able to create token", "success": False}
    else:
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": {
                "fullname": user.full_name,
                "message": "user logged in successfully",
                "code": 200,
                "status": True
            }
        }


@app_v1.post("/doctors/forgot-password/{through}", tags=["DOCTORS/GENERAL"])
async def forget_password(request: ForgotPassword, through: str = Path(..., title="to check whether user has logged "
                                                                                  "in through mail/phone")):
    if through == "mail":
        result = await find_exist_username_email(check=request.mail)
        if not result:
            return {"status": 404, "message": "Doctor/Therapist not found", "success": False}
    elif through == "phone_number":
        result = await find_exist_user_phone(phone_number=request.phone_number)
        if not result:
            return {"status": 404, "message": "User not found", "success": False}
    else:
        logger.error("###### ERROR IN PATH PARAMETER NOT DEFINED ####### ")
        return {"status": 404, "message": "Error in path param", "success": True}

    # create reset code and save into database
    reset_code = str(uuid.uuid1())
    try:
        await create_reset_code(request.mail, reset_code)

        # message = MessageSchema(
        #     subject="Forgot Password !!",
        #     recipients=[request.mail],
        #     body="You have requested for reset password, Please find the instructions below \n Enter the code "
        #          "provided below \n code: {}".format(
        #         reset_code),
        #     subtype="html"
        # )
        # conf = Connection()
        # fm = FastMail(conf.conf)
        try:
            logger.info("#### SENDING RESET PASSWORD MESSAGE ON THE MAIL {} ########".format(request.mail))
            # await fm.send_message(message)
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
            return {
                "code": 401,
                "message": "Error, email not send",
                "success": False
            }
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
        return {"status": 409, "message": "Reset password token has expired,please request a new one", "success": False}

    # Check if both new & confirm password are same
    if request.new_password != request.confirm_password:
        logger.error("###### NEW PASSWORD AND CONFIRM PASSWORD ARE NOT A MATCH ######### ")
        return {"status": 409, "message": "Password didn't match", "success": False}

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


# @app_v1.put("/doctors/image-upload/{username}", tags=["DOCTORS/GENERAL"])
# async def uploading_image(username: str, file: bytes = File(...)):
#     try:
#         logger.info("######## UPDATING IMAGE FOR THE DOCTOR/THERAPIST {} ####".format(username))
#         # Check if username exist or not
#         result_obj = await find_exist_username(username=username)
#         if result_obj is not None:
#             logger.info("#### USERNAME IS VALID #####")
#             result = cloudinary.uploader.upload(file)
#             url = result.get("url")
#             # await update_profile_picture(username=username, url=url)
#             return {
#                 "status": status.HTTP_201_CREATED,
#                 "message": "Image uploaded successfully",
#                 "url":url,
#                 "success": True
#             }
#         else:
#             return {"error":
#                 {
#                     "message": "No user found",
#                     "code": status.HTTP_404_NOT_FOUND,
#                     "success": False,
#                     "target": "Image-Upload[CHECK-USERNAME]"
#                 }
#             }
#     except Exception as e:
#         logger.error("######## EXCEPTION OCCURED IN IMAGE UPLOAD METHOD {} FOR USER ###### ".format(e, username))
#     finally:
#         logger.info("####### UPLOADING IMAGE METHOD COMPLETED ######")


@app_v1.put("/doctors/image-upload", tags=["DOCTORS/GENERAL"])
async def uploading_image(file: bytes = File(...)):
    try:
        logger.info("######## UPDATING IMAGE FOR THE DOCTOR/THERAPIST {} ####")
        logger.info("#### USERNAME IS VALID #####")
        result = cloudinary.uploader.upload(file)
        url = result.get("url")
        return {
            "status": status.HTTP_201_CREATED,
            "message": "Image uploaded successfully",
            "url": url,
            "success": True
        }
    except Exception as e:
        logger.error("######## EXCEPTION OCCURED IN IMAGE UPLOAD METHOD {} ###### ".format(e))
    finally:
        logger.info("####### UPLOADING IMAGE METHOD COMPLETED ######")
