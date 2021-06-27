from fastapi import status, APIRouter
from constants.const import UPDATE, WHERE, TIME_SLOT_ID_KEY
from utils.logger.logger import logger
from utils.db_functions.db_functions import \
    save_time_slot_config, save_timeSlot_doctor_map, find_time_slot, get_time_slot_configuration, find_booked_time_slot, \
    update_time_slot, add_timeslot_combined_function, find_doctors_timeslot_schedule, find_if_doctor_exist_in_timeslot, \
    update_time_slot_for_doctor, time_slot_for_day, time_slot_for_all_days, find_booked_time_slots, \
    find_if_time_slot_exist
from fastapi import Body
from models.time_slot_configuration import TimeSlot, TimeSlotUpdate, Status
from fastapi import Path, Query
from typing import List
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.utils_classes.classes_for_checks import CheckUserExistence, CheckTimeSlotId, TimeslotConfiguration, \
    CheckForConsultation
from datetime import datetime, timezone

dt = datetime.now(timezone.utc)

doctor_time_slot_routes = APIRouter()


@doctor_time_slot_routes.post("/doctors/time-slot", tags=["DOCTOR/TIME-SLOT"])
async def time_slot_mapping(time_slot_config: List[TimeSlot], doctor_id: int = Body(..., description="doctor id")):
    logger.info("##### POST CALL FOR DOCTOR TIME-SLOT CONFIG ######### ")
    response = CheckUserExistence(_id=doctor_id, target="POST[DOCTOR-TIMESLOT]")
    await response.check_if_user_id_exist()
    """ CHECK TO FIND IF CONFIGURATION EXIST OR NOT """
    check_if_doctor_exist = await find_if_doctor_exist_in_timeslot(doctor_id=doctor_id)
    if check_if_doctor_exist is not None:
        raise CustomExceptionHandler(message="Configuration for the doctor already exit",
                                     success=False,
                                     target="Save Timeslot",
                                     code=status.HTTP_400_BAD_REQUEST)
    days = []
    for check_unique_day in time_slot_config:
        if check_unique_day in days:
            logger.error("####### SAME DAY CANNOT BE PROVIDED ###########")
            raise CustomExceptionHandler(
                message="Same day configuration provided for doctor id= {}".format(str(doctor_id)),
                success=False,
                target="Save Timeslot",
                code=status.HTTP_400_BAD_REQUEST)
        else:
            days.append(check_unique_day)

    map_array_objects = []
    for time_values in time_slot_config:
        time_configuration_object = TimeslotConfiguration(start_time=time_values.start_time,
                                                          end_time=time_values.end_time,
                                                          doctor_id=doctor_id)
        time_configuration_object.time_slot_configuration_checks()
        success = await add_timeslot_combined_function(val=time_values,
                                                       doctor_id=doctor_id,
                                                       map_array_objects=map_array_objects)
        if not success:
            raise CustomExceptionHandler(message="Unable to save timeslot for doctor id {}".format(str(doctor_id)),
                                         success=False,
                                         target="Save Timeslot",
                                         code=status.HTTP_400_BAD_REQUEST)
    return {"message": "Successfully inserted in timeslot doctor map",
            "success": True,
            "code": status.HTTP_201_CREATED}


""" ROLLBACK IN THIS ROUTE AND ALSO CHECK FOR SAME DAY MULTIPLE VALUES """

global object_id


@doctor_time_slot_routes.put("/doctors/time-slot", tags=["DOCTOR/TIME-SLOT"])
async def time_slot_update(time_slot_config: List[TimeSlotUpdate],
                           doctor_id: int = Body(None, description="doctor id")):
    global object_id
    logger.info("##### PUT CALL FOR DOCTOR TIME-SLOT CONFIG ######### ")
    response = CheckUserExistence(_id=doctor_id, target="POST[DOCTOR-TIMESLOT]")
    await response.check_if_user_id_exist()

    """IF USER WANTS TO UPDATE EXISTING TIMESLOT """
    map_array_objects = []
    for find_time_slot_id in time_slot_config:
        if not find_time_slot_id.time_slot_id:
            days = []
            for check_unique_day in time_slot_config:
                if check_unique_day in days:
                    logger.error("####### SAME DAY CANNOT BE PROVIDED ###########")
                    raise CustomExceptionHandler(
                        message="Same day configuration provided for doctor id= {}".format(str(doctor_id)),
                        success=False,
                        target="Save Timeslot",
                        code=status.HTTP_400_BAD_REQUEST)
                else:
                    days.append(check_unique_day)
            time_configuration_object = TimeslotConfiguration(start_time=find_time_slot_id.start_time,
                                                              end_time=find_time_slot_id.end_time,
                                                              doctor_id=doctor_id)
            time_configuration_object.time_slot_configuration_checks()

            time_slot_exist = await find_if_time_slot_exist(doctor_id=doctor_id,
                                                            time=find_time_slot_id.start_time.date())
            if time_slot_exist is not None:
                raise CustomExceptionHandler(
                    message="Timeslot for doctor id {} already exist, please make an update call ".format(str(doctor_id)),
                    success=False,
                    target="Save Timeslot",
                    code=status.HTTP_400_BAD_REQUEST)

            success = await add_timeslot_combined_function(val=find_time_slot_id,
                                                           doctor_id=doctor_id,
                                                           map_array_objects=map_array_objects)
            if not success:
                raise CustomExceptionHandler(message="Unable to save timeslot for doctor id {}".format(str(doctor_id)),
                                             success=False,
                                             target="Save Timeslot",
                                             code=status.HTTP_400_BAD_REQUEST)

        try:
            if find_time_slot_id.time_slot_id:
                response = CheckTimeSlotId(_id=find_time_slot_id.time_slot_id, target="PUT-TIMESLOT-HAS_ID")
                await response.check_id_exist()

                # todo: couple start time and end time, if user only wants to change start_time and end_time

                time_configuration_object = TimeslotConfiguration(start_time=find_time_slot_id.start_time,
                                                                  end_time=find_time_slot_id.end_time,
                                                                  doctor_id=doctor_id)
                time_configuration_object.time_slot_configuration_checks()

                # TODO: DAY CHECKS REMAINING
                doctor_time_map = {"start_time": find_time_slot_id.start_time, "end_time": find_time_slot_id.end_time}
                consultation_check_object = CheckForConsultation(doctor_id=doctor_id,
                                                                 time_slot_id=find_time_slot_id.time_slot_id,
                                                                 doctor_time_map=doctor_time_map)
                await consultation_check_object.end_time()
                await consultation_check_object.start_time()
                query_for_update = UPDATE
                update_values_map = {}
                for key in find_time_slot_id:
                    if key[0] == TIME_SLOT_ID_KEY:
                        update_values_map["id"] = key[1]
                        continue
                    if key[1] is None:
                        continue
                    update_values_map[key[0]] = key[1]
                    query_for_update = query_for_update + key[0] + "".join("=:") + key[0] + ","
                query_for_update = query_for_update.rstrip(",")
                query_for_update = query_for_update + WHERE

                await update_time_slot_for_doctor(query_object_for_update=query_for_update,
                                                  update_value_map=update_values_map)

        except Exception as WHY:
            logger.error(
                "#### EXCEPTION IN UPDATE CALL FOR DOCTOR TIMESLOT BECAUSE {} FOR DOCTOR ID {} ####".format(WHY,
                                                                                                            doctor_id))
            raise CustomExceptionHandler(message="Unable to save timeslot for doctor id {}".format(str(doctor_id)),
                                         success=False,
                                         target="Save Timeslot",
                                         code=status.HTTP_400_BAD_REQUEST)

    return {"success"}


@doctor_time_slot_routes.get("/doctors/time-slot/{doctor_id}", tags=["DOCTOR/TIME-SLOT"])
async def get_timeslot_specific_doctor(doctor_id: int = Path(...),
                                       day: Status = Query(None, description="Query parameter for days")):
    response = CheckUserExistence(_id=doctor_id, target="GET-AVAILABLE-TIMESLOT FOR SPECIFIC DOCTOR")
    await response.check_if_user_id_exist()
    if day:
        return {"doctor_slots": await time_slot_for_day(doctor_id=doctor_id, day=day),
                "booked": {day: await find_booked_time_slot(doctor_id=doctor_id, day=day)}
                }
    else:
        return {"doctor_slots": await time_slot_for_all_days(doctor_id=doctor_id),
                "booked": await find_booked_time_slots(doctor_id=doctor_id)
                }
