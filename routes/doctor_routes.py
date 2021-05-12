from fastapi import status, APIRouter, HTTPException, Depends, File
from utils.security.security import verify_password, hash_password
from models.doctor import Doctor, DoctorUpdate, ChangePassword, ChannelName
from utils.jwt_utils.jwt_utils import get_current_user, get_token_user
from utils.logger.logger import logger
from conferencing.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee, Role_Publisher
import time
from constants import const
from utils.random_generator.random_digits import random_with_N_digits
from utils.db_functions.db_functions import find_exist_user, get_doctor_information
from utils.db_functions.doctor_crud import change_password_user, save_black_list_token

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


@doctor_routes.get("/doctors/profile", tags=['DOCTORS/RESTRICTED'])
async def get_user_profile(current_user: Doctor = Depends(get_current_user)):
    try:
        result_db = {"mail": current_user.mail, "full_name": current_user.full_name,
                     "phone_number": current_user.phone_number}
        return result_db
    except Exception as e:
        logger.error("#### ERROR IN GET USER PROFILE ROUTE {} ##### ".format(e))


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


@doctor_routes.patch("/doctors/qualification-update", tags=["DOCTORS/RESTRICTED"])
async def update_qualification(current_user: Doctor = Depends(get_current_user)):
    const = await get_doctor_information(current_user.username)
    const = dict(const)
    print(const)