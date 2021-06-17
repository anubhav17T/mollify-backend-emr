from fastapi import status, APIRouter
from constants.const import UPDATE, WHERE
from utils.logger.logger import logger
from utils.db_functions.db_functions import \
    save_time_slot_config, save_timeSlot_doctor_map, find_time_slot, get_time_slot_configuration, find_booked_time_slot, \
    update_time_slot
from fastapi import Body
from models.time_slot_configuration import TimeSlot, TimeSlotUpdate
from fastapi import Path
from typing import List
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.utils_classes.classes_for_checks import CheckUserExistence, CheckTimeSlotId

doctor_time_slot_routes = APIRouter()


@doctor_time_slot_routes.post("/doctors/time-slot", tags=["DOCTOR/TIME-SLOT"])
async def time_slot_mapping(time_slot_config: List[TimeSlot], doctor_id: int = Body(..., description="doctor id")):
    global object_id
    logger.info("##### POST CALL FOR DOCTOR TIME-SLOT CONFIG ######### ")
    response = CheckUserExistence(_id=doctor_id, target="POST[DOCTOR-TIMESLOT]")
    await response.check_if_user_id_exist()

    map_array_objects = []
    for time_values in time_slot_config:
        print(time_values)

        object_id = await save_time_slot_config(val=time_values)
        map_object = {"doctor_id": doctor_id,
                      "time_slot_id": object_id
                      }
        map_array_objects.append(map_object)
    logger.info(
        "### TIME SLOT CONFIGURATION FOR THE DOCTOR ID {} HAS BEEN UPDATED SUCCESSFULLY WITH OBJECT ID  "
        "####".format(
            str(doctor_id)))
    await save_timeSlot_doctor_map(map_array_objects)
    return {"message": "Inserted success in timeslot doctor map", "success": True,
                "code": status.HTTP_201_CREATED}



""" ROLLBACK IN THIS ROUTE AND ALSO CHECK FOR SAME DAY MULTIPLE VALUES """

global object_id
from utils.connection_configuration.db_object import db


@doctor_time_slot_routes.put("/doctors/time-slot", tags=["DOCTOR/TIME-SLOT"])
async def time_slot_update(time_slot_config: List[TimeSlotUpdate],
                           doctor_id: int = Body(None, description="doctor id")):
    global object_id
    logger.info("##### PUT CALL FOR DOCTOR TIME-SLOT CONFIG ######### ")

    """IF USER WANTS TO UPDATE EXISTING TIMESLOT """
    for find_time_slot_id in time_slot_config:
        if find_time_slot_id.time_slot_id:
            response = CheckTimeSlotId(_id=find_time_slot_id.time_slot_id, target="PUT-TIMESLOT-HASID")
            await response.check_id_exist()
            query_for_update = UPDATE
            update_values_map = {}
            for key in find_time_slot_id:
                if key[0] == "time_slot_id":
                    update_values_map["id"] = key[1]
                    continue
                if key[1] is None:
                    continue
                update_values_map[key[0]] = key[1]
                query_for_update = query_for_update + key[0] + "".join("=:") + key[0] + ","
            query_for_update = query_for_update.rstrip(",")
            query_for_update = query_for_update + WHERE
            check_response = await update_time_slot(query_object=query_for_update,
                                                    update_value_map=update_values_map)

            if check_response is None:
                raise CustomExceptionHandler(
                    message="Cannot able to update the time-slot config for given id {}".format(
                        find_time_slot_id.time_slot_id),
                    code=status.HTTP_400_BAD_REQUEST,
                    success=False,
                    target="PUT-TIMESLOT-CONFIG[HAS TIMESLOT ID]"
                )

        # If new entry then pass as follows
        if not find_time_slot_id.time_slot_id:
            if doctor_id is not None:
                response = CheckUserExistence(_id=doctor_id, target="POST[DOCTOR-TIMESLOT]")
                await response.check_if_user_id_exist()
                map_array_objects = []
                try:
                    object_id = await save_time_slot_config(val=find_time_slot_id)
                    map_object = {"doctor_id": doctor_id,
                                  "time_slot_id": object_id
                                  }
                    map_array_objects.append(map_object)
                except Exception as E:
                    logger.error(
                        "#### SOMETHING WENT WRONG IN THE CREATE NEW TIMESLOT WITH DOCTORID BECAUSE {}".format(E))
                    raise CustomExceptionHandler(
                        message="Cannot able to update the time-slot config for given id {}".format(
                            find_time_slot_id.time_slot_id),
                        code=status.HTTP_400_BAD_REQUEST,
                        success=False,
                        target="PUT-TIMESLOT-CONFIG[HAS TIMESLOT ID]"
                    )


@doctor_time_slot_routes.get("/doctors/time-slot/{doctor_id}", tags=["DOCTOR/TIME-SLOT"])
async def get_all_timeslot(doctor_id: int = Path(...)):
    logger.info("##### DOCTOR ALL TIME SLOT #########")
    response = CheckUserExistence(_id=doctor_id, target="GET-TIMESLOT FOR SPECIFIC DOCTOR")
    await response.check_if_user_id_exist()
    return await get_time_slot_configuration(doctor_id=doctor_id)


@doctor_time_slot_routes.get("/doctors/available/time-slot/{doctor_id}", tags=["DOCTOR/TIME-SLOT"])
async def get_timeslot_specific_doctor(doctor_id: int = Path(...)):
    response = CheckUserExistence(_id=doctor_id, target="GET-AVAILABLE-TIMESLOT FOR SPECIFIC DOCTOR")
    await response.check_if_user_id_exist()

    fetch_available_timeslots = await find_time_slot(doctor_id=doctor_id)
    find_booked_time_slots = await find_booked_time_slot(doctor_id=doctor_id)
    return {"all_time_slot": fetch_available_timeslots, "booked": find_booked_time_slots}
