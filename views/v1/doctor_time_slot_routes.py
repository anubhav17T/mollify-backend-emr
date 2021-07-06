from fastapi import status, APIRouter
from constants.const import UPDATE, WHERE, TIME_SLOT_ID_KEY, DOCTOR_ID_KEY
from utils.db_functions.raw_queries import INSERT_QUERY_FOR_TIMESLOT, QUERY_FOR_DOCTOR_TIMESLOT_MAP
from utils.logger.logger import logger
from utils.db_functions.db_functions import find_booked_time_slot, find_if_doctor_exist_in_timeslot, \
    update_time_slot_for_doctor, time_slot_for_day, time_slot_for_all_days, find_booked_time_slots, \
    find_if_time_slot_exist, execute_insertion_for_timeslot, \
    execute_insertion_in_doctor_time_slot_map, execute_sample
from fastapi import Body
from models.time_slot_configuration import TimeSlot, TimeSlotUpdate, Status
from fastapi import Path, Query
from typing import List
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.utils_classes.classes_for_checks import CheckUserExistence, CheckTimeSlotId, TimeslotConfiguration, \
    CheckForConsultation
from datetime import datetime, timezone
from utils.connection_configuration.db_object import db

dt = datetime.now(timezone.utc)
global object_id

doctor_time_slot_routes = APIRouter()


@doctor_time_slot_routes.post("/doctors/time-slot", tags=["DOCTOR/TIME-SLOT"])
async def time_slot_mapping(time_slot_config: List[TimeSlot], doctor_id: int = Body(..., description="doctor id")):
    logger.info("##### POST CALL FOR DOCTOR TIME-SLOT CONFIG ######### ")
    response = CheckUserExistence(_id=doctor_id, target="POST[DOCTOR-TIMESLOT]")
    await response.check_if_user_id_exist()
    """ CHECK TO FIND IF CONFIGURATION EXIST OR NOT """
    check_if_doctor_exist = await find_if_doctor_exist_in_timeslot(doctor_id=doctor_id)
    if check_if_doctor_exist is not None:
        raise CustomExceptionHandler(message="Configuration for the doctor already exist,please use update call",
                                     success=False,
                                     target="Save Timeslot",
                                     code=status.HTTP_400_BAD_REQUEST)
    async with db.transaction():
        transaction = await db.transaction()
        try:
            days = []
            for check_unique_day in time_slot_config:
                if check_unique_day in days:
                    logger.error("####### SAME DAY CANNOT BE PROVIDED FOR DOCTOR ID ###########".format(str(doctor_id)))
                    raise Exception("You have provided same day timeslots twice.")
                else:
                    days.append(check_unique_day)

            for time_values in time_slot_config:
                if time_values.start_time is None or time_values.end_time is None:
                    raise Exception("Please specify start time and end time value!")

                if time_values.buffer_time <= 5:
                    raise Exception("Buffer time should be greater than 5")

                time_configuration_object = TimeslotConfiguration(start_time=time_values.start_time,
                                                                  end_time=time_values.end_time,
                                                                  doctor_id=doctor_id)

                time_configuration_object.check_if_start_time_greater_than_end_time()
                time_configuration_object.check_if_start_date_greater_than_end_date()
                time_configuration_object.check_if_start_date_valid()

                logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY TIMESLOT ADD CALL #######")
                time_slot_exist = await find_if_time_slot_exist(doctor_id=doctor_id,
                                                                day=time_values.day)
                if time_slot_exist:
                    raise Exception(
                        "Timeslot already exist for the day provided for doctorId = {}".format(doctor_id))
                id_for_timeslot_config = await execute_insertion_for_timeslot(configuration_hash_map=time_values)
                if id_for_timeslot_config is None:
                    raise Exception("cannot find the id for the doctor")
                map_object = {DOCTOR_ID_KEY: doctor_id,
                              TIME_SLOT_ID_KEY: id_for_timeslot_config
                              }
                logger.info(
                    "### TIME SLOT CONFIGURATION FOR THE DOCTOR ID {} HAS BEEN UPDATED SUCCESSFULLY WITH OBJECT ID  "
                    "####".format(
                        str(doctor_id)))
                await execute_insertion_in_doctor_time_slot_map(configuration_map=map_object)

        except Exception as WHY:
            logger.error(
                "######## EXCEPTION OCCURRED IN ADD TIMESLOT CONFIGURATION FOR DOCTOR_ID {} DUE TO {} ####".format(
                    str(doctor_id), WHY))
            logger.error("###### ROLLING BACK THE QUERY ###########")
            await transaction.rollback()
            raise CustomExceptionHandler(
                message="Unable to update the timeslot map for the doctor because: {} ".format(
                    WHY),
                success=False,
                code=status.HTTP_400_BAD_REQUEST,
                target="Update timeslot for doctor"
            )
        else:
            logger.info("##### ALL WENT WELL COMMITTING TRANSACTION ########")
            await transaction.commit()
            return {"message": "Successfully inserted in timeslot doctor map",
                    "success": True,
                    "code": status.HTTP_201_CREATED}


@doctor_time_slot_routes.get("/doctors/time-slot/{doctor_id}", tags=["DOCTOR/TIME-SLOT"])
async def get_timeslot_specific_doctor(doctor_id: int = Path(...),
                                       day: Status = Query(None, description="Query parameter for days")):
    response = CheckUserExistence(_id=doctor_id, target="GET-AVAILABLE-TIMESLOT FOR SPECIFIC DOCTOR")
    await response.check_if_user_id_exist()
    try:
        if day:
            return {"doctor_slots": await time_slot_for_day(doctor_id=doctor_id, day=day),
                    "booked": await find_booked_time_slot(doctor_id=doctor_id, day=day)
                    }
        else:
            return {"doctor_slots": await time_slot_for_all_days(doctor_id=doctor_id),
                    "booked": await find_booked_time_slots(doctor_id=doctor_id)
                    }
    except Exception as WHY:
        logger.error("######### ERROR OCCURRED WHILE GETTING TIMESLOTS FOR DOCTOR DUE TO {} FOR DOCTOR_ID {} "
                     "###########".format(WHY, doctor_id))
        raise CustomExceptionHandler(
            message="UNABLE TO GET TIMESLOTS FOR DOCTOR_ID {} DUE TO {}".format(str(doctor_id), WHY),
            success=False,
            target="Save Timeslot",
            code=status.HTTP_400_BAD_REQUEST)
    finally:
        logger.info("####### METHOD TO GET TIMESLOTS IS FINISHED ##########")


@doctor_time_slot_routes.get("/doctors/sample/", tags=["DOCTOR/TIME-SLOT"])
async def return_sample():
    return await execute_sample()


@doctor_time_slot_routes.put("/doctors/time-slot", tags=["DOCTOR/TIME-SLOT"])
async def time_slot_update(time_slot_config: List[TimeSlotUpdate],
                           doctor_id: int = Body(None, description="doctor id")):
    global object_id
    logger.info("##### UPDATE METHOD CALLED FOR TIMESLOT CONFIGURATION ######### ")
    response = CheckUserExistence(_id=doctor_id, target="POST[DOCTOR-TIMESLOT]")
    await response.check_if_user_id_exist()
    logger.info("####### DOCTOR/THERAPIST EXIST PROCEEDING FURTHER ###########")

    async with db.transaction():
        transaction = await db.transaction()
        try:
            for configuration_for_time in time_slot_config:
                if configuration_for_time.id:
                    response = CheckTimeSlotId(_id=configuration_for_time.id, target="PUT-TIMESLOT-HAS_ID")
                    await response.check_id_exist()

                    if configuration_for_time.start_time is None or configuration_for_time.end_time is None:
                        raise Exception("Please specify start time and end time value!")
                    if configuration_for_time.buffer_time is not None and configuration_for_time.buffer_time <= 5:
                        raise Exception("Buffer time should be greater than 5")

                    time_configuration_object = TimeslotConfiguration(start_time=configuration_for_time.start_time,
                                                                      end_time=configuration_for_time.end_time,
                                                                      doctor_id=doctor_id)

                    time_configuration_object.check_if_start_time_greater_than_end_time()
                    time_configuration_object.check_if_start_date_greater_than_end_date()
                    time_configuration_object.check_if_start_date_valid()

                    # TODO: DAY CHECKS REMAINING
                    doctor_time_map = {"start_time": configuration_for_time.start_time,
                                       "end_time": configuration_for_time.end_time}
                    consultation_check_object = CheckForConsultation(doctor_id=doctor_id,
                                                                     time_slot_id=configuration_for_time.id,
                                                                     doctor_time_map=doctor_time_map)
                    await consultation_check_object.end_time()
                    await consultation_check_object.start_time()

                    query_for_update = UPDATE
                    update_values_map = {}
                    for key in configuration_for_time:
                        if key[0] == TIME_SLOT_ID_KEY:
                            update_values_map["id"] = key[1]
                            continue
                        if key[1] is None:
                            continue
                        update_values_map[key[0]] = key[1]
                        query_for_update = query_for_update + key[0] + "".join("=:") + key[0] + ","
                    query_for_update = query_for_update.rstrip(",")
                    query_for_update = query_for_update + WHERE
                    logger.info("###### PROCEEDING FOR THE UPDATE TIMESLOT CONFIGURATION ##########")
                    await db.execute(query=query_for_update, values=update_values_map)
                    logger.info("#### SUCCESS IN UPDATE CALL #####")

                if not configuration_for_time.id:
                    days = []
                    for check_unique_day in time_slot_config:
                        if check_unique_day in days:
                            logger.error(
                                "####### SAME DAY CANNOT BE PROVIDED FOR DOCTOR ID ###########".format(str(doctor_id)))
                            raise Exception("You have provided same day timeslots twice.")
                        else:
                            days.append(check_unique_day)

                    logger.info("##### DAYS ARE UNIQUE ##########")
                    if configuration_for_time.start_time is None or configuration_for_time.end_time is None:
                        raise Exception("Please specify start time and end time value!")

                    time_configuration_object = TimeslotConfiguration(start_time=configuration_for_time.start_time,
                                                                      end_time=configuration_for_time.end_time,
                                                                      doctor_id=doctor_id)

                    time_configuration_object.check_if_start_time_greater_than_end_time()
                    time_configuration_object.check_if_start_date_greater_than_end_date()
                    time_configuration_object.check_if_start_date_valid()

                    time_slot_exist = await find_if_time_slot_exist(doctor_id=doctor_id,
                                                                    day=configuration_for_time.day)
                    if time_slot_exist:
                        raise Exception(
                            "Timeslot already exist for the date provided for doctorId = {}".format(doctor_id))
                    id_for_timeslot_config = await execute_insertion_for_timeslot(
                        configuration_hash_map=configuration_for_time)
                    if id_for_timeslot_config is None:
                        raise Exception("cannot find the id for the doctor")
                    map_object = {DOCTOR_ID_KEY: doctor_id,
                                  TIME_SLOT_ID_KEY: id_for_timeslot_config
                                  }
                    logger.info(
                        "### TIME SLOT CONFIGURATION FOR THE DOCTOR ID {} HAS BEEN "
                        "UPDATED SUCCESSFULLY WITH OBJECT ID "
                        "####".format(
                            str(doctor_id)))
                    await execute_insertion_in_doctor_time_slot_map(configuration_map=map_object)

        except Exception as WHY:
            logger.error("######### ERROR IN THE QUERY BECAUSE {} ".format(WHY))
            logger.info("########## ROLLING BACK TRANSACTIONS #################")
            await transaction.rollback()
            raise CustomExceptionHandler(
                message="Unable to update the timeslot map for the doctor id {} BECAUSE of exception = {} ".format(
                    doctor_id, WHY),
                success=False,
                code=status.HTTP_400_BAD_REQUEST,
                target="Update timeslot for doctor"
            )
        else:
            logger.info("##### ALL WENT WELL COMMITTING TRANSACTION ########")
            await transaction.commit()
            logger.info("###### TRANSACTION COMMITTED AND SUCCESS TRUE #######")
            return {"message": "Successfully updated Timeslot configuration",
                    "success": True,
                    "code": status.HTTP_201_CREATED}
