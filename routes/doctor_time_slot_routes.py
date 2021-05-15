from fastapi import Request
import re
from fastapi import status, APIRouter, HTTPException, Depends, UploadFile, File
from utils.logger.logger import logger
from utils.db_functions.db_functions import find_exist_username_email, find_exist_user_id, find_exist_username, \
    find_exist_user_phone, find_slug_therapist, save_doctor, create_reset_code, check_reset_password_token, \
    reset_password_user, disable_reset_code, update_profile_picture, get_doctor_information, save_qualification, \
    save_specialisation, get_sepecific_specialisation, get_all_specialisation, save_specialisation_map, get_all_doctor, \
    save_time_slot_config, save_timeSlot_doctor_map
from fastapi import Body
from models.time_slot_configuration import TimeSlot
from fastapi import Query
from typing import List

doctor_time_slot_routes = APIRouter()


@doctor_time_slot_routes.post("/doctors/time-slot", tags=["DOCTOR/TIME-SLOT"])
async def time_slot_mapping(time_slot_config: List[TimeSlot], doctor_id: int = Body(..., description="doctor id")):
    global object_id
    logger.info("##### POST CALL FOR DOCTOR TIME-SLOT CONFIG ######### ")
    try:
        find_doctor_id = await find_exist_user_id(id=doctor_id)
        if find_doctor_id is None:
            return {"error": {"message": "cannot able to find the doctor with provided id",
                              "code": status.HTTP_404_NOT_FOUND,
                              "success": False,
                              "target": "POST[DOCTOR-TIMESLOT]"
                              }}
        map_array_objects = []
        for time_values in time_slot_config:
            object_id = await save_time_slot_config(val=time_values)
            map_object = {"doctor_id": doctor_id,
                          "time_slot_id": object_id
                          }
            map_array_objects.append(map_object)
        print(map_array_objects)
        logger.info(
            "### TIME SLOT CONFIGURATION FOR THE DOCTOR ID {} HAS BEEN UPDATED SUCCESSFULLY WITH OBJECT ID  "
            "####".format(
                str(doctor_id)))
        await save_timeSlot_doctor_map(map_array_objects)
        return {"message": "inserted success in timeslot doctor map", "success": True,
                "code": status.HTTP_201_CREATED}
    except Exception as e:
        return {"error": {"message": "error occurred because of {}".format(e),
                          "code": status.HTTP_400_BAD_REQUEST,
                          "success": False,
                          "target": "POST[TIMESLOT-DOCTOR0-MAP]"}}
