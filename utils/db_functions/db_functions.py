import json

from models.doctor import Doctor
from models.languages import LanguagesUpdate
from utils.db_functions.raw_queries import QUERY_FOR_REGISTER_DOCTOR, QUERY_FOR_SAVE_SPECIALISATION, \
    QUERY_FOR_SAVE_LANGUAGE, QUERY_FOR_SAVE_QUALIFICATION, QUERY_FOR_SPECIALISATION_MAP
from utils.logger.logger import logger
from utils.connection_configuration.db_object import db
from datetime import datetime, timezone
from models.specialisation import Specialisation
from models.doctor_specialisation import DoctorSpecialisation


def save_specialisation(specailisations:Specialisation):
    try:
        query = """INSERT INTO specialisations VALUES (nextval('specialisations_id_seq'),:name,:is_active,now() at time zone 'UTC') """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF SPECIALISATION")
        return db.execute(query, values={"name": specailisations.name,
                                         "is_active": True})
    except Exception as e:
        logger.error("##### EXCEPTION IN SAVE_SPECIALISATION FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### FIND SAVE_SPECIALISATION FUNCTION COMPLETED ####")


def save_languages(languages: LanguagesUpdate):
    try:
        query = """INSERT INTO languages VALUES (nextval('languages_id_seq'),:name,:is_active,now() at time zone 
        'UTC') """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF LANGUAGES")
        return db.execute(query, values={"name": languages.name,
                                         "is_active": languages.is_active})
    except Exception as e:
        logger.error("##### EXCEPTION IN SAVE_LANGUAGE FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### FIND SAVE_LANGUAGE FUNCTION COMPLETED ####")


def find_particular_language(name):
    try:
        query = "SELECT * FROM languages WHERE name=:name"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF FINDING PARTICULAR ####")
        return db.fetch_one(query=query, values={"name": name})
    except Exception as e:
        logger.error("##### EXCEPTION IN SAVE_LANGUAGE FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND PARTICULAR_LANGUAGE FUNCTION COMPLETED ####")


def get_specific_doctor(search_query):
    try:
        query = """ SELECT * FROM doctors WHERE mail=:mail or username=:username """
        logger.info("### PROCEEDING FURTHER FOR EXECUTION OF QUERY OF GET SPECIFIC DOCTOR")
        return db.fetch_one(query, values={"mail": search_query, "username": search_query})
    except Exception as e:
        logger.error("#### EXCEPTION IN GET SPECIFIC DOCTOR IS {} #####".format(e))


def get_all_doctor():
    try:
        query = """ SELECT * FROM doctors LIMIT 10"""
        logger.info("### PROCEEDING FURTHER FOR EXECUTION OF QUERY OF GET SPECIFIC DOCTOR")
        return db.fetch_all(query)
    except Exception as e:
        logger.error("#### EXCEPTION IN GET SPECIFIC DOCTOR IS {} #####".format(e))


def doctor_by_name(name: str):
    name = name + str('%')
    query = """ SELECT * FROM doctors WHERE full_name LIKE '{}' """.format(name)
    try:
        logger.info("### FETCHING ALL THE RESULTS ######")
        return db.fetch_all(query)
    except Exception as e:
        logger.error("#### EXCEPTION IN GET SPECIFIC DOCTOR IS {} #####".format(e))


def get_sepecific_specialisation(state: str):
    try:
        query = "select * from specialisations where is_active=:is_active"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET SPECIALISATION")
        return db.fetch_all(query, values={"is_active": bool(state)})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_SPECIALISATION FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_SPECIALISATION FUNCTION COMPLETED ####")


def get_true_specialisation():
    try:
        query = "select * from specialisations where is_active=:is_active order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET SPECIALISATION")
        return db.fetch_all(query, values={"is_active": True})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_SPECIALISATION FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_SPECIALISATION FUNCTION COMPLETED ####")


def get_true_languages():
    try:
        query = "select * from languages where is_active=:is_active order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET LANGUAGES")
        return db.fetch_all(query, values={"is_active": True})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_SPECIALISATION FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_SPECIALISATION FUNCTION COMPLETED ####")


def get_false_specialisation():
    try:
        query = "select * from specialisations where is_active=:is_active order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET SPECIALISATION")
        return db.fetch_all(query, values={"is_active": False})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_SPECIALISATION FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_SPECIALISATION FUNCTION COMPLETED ####")


def get_false_languages():
    try:
        query = "select * from languages where is_active=:is_active order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET SPECIALISATION")
        return db.fetch_all(query, values={"is_active": False})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_SPECIALISATION FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_SPECIALISATION FUNCTION COMPLETED ####")


def get_all_specialisation():
    try:
        query = "select * FROM specialisations order by created_on desc"""
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET SPECIALISATION")
        return db.fetch_all(query)
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_SPECIALISATION FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### GET_ALL_SPECIALISATION FUNCTION COMPLETED ####")


def get_all_languages():
    try:
        query = "select * FROM languages order by created_on desc"""
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET SPECIALISATION")
        return db.fetch_all(query)
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_SPECIALISATION FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### GET_ALL_SPECIALISATION FUNCTION COMPLETED ####")


def find_exist_user(mail: str):
    try:
        query = "select * from doctors where mail=:mail"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.fetch_one(query=query, values={"mail": mail})
    except Exception as e:
        logger.error("##### EXCEPTION IN FIND_EXIST_USER FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND EXIST USER FUNCTION COMPLETED ####")


def find_exist_user_id(id: int):
    try:
        query = "select * from doctors where id=:id"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.fetch_one(query=query, values={"id": id})
    except Exception as e:
        logger.error("##### EXCEPTION IN FIND_EXIST_USER_ID FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND EXIST USER WITH ID FUNCTION COMPLETED ####")


def find_exist_username_email(check: str):
    try:
        query = "select * from doctors where mail=:mail or username=:username"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.fetch_one(query=query, values={"mail": check, "username": check})
    except Exception as e:
        logger.error("##### EXCEPTION IN FIND_EXIST_USER FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND EXIST MAIL/USERNAME FUNCTION COMPLETED ####")


def find_exist_username(username: str):
    try:
        query = "select * from doctors where username=:username"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.fetch_one(query=query, values={"username": username})
    except Exception as e:
        logger.error("##### EXCEPTION IN FIND_EXIST_USERNAME FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND EXIST USER FUNCTION COMPLETED ####")


def find_exist_user_phone(phone_number: str):
    try:
        query = "SELECT * FROM doctors WHERE phone_number=:phone_number"
        logger.info("##### PROCEEDING FURTHER FOR THE FINDING EXIST PHONE NUMBER ####")
        return db.fetch_one(query=query, values={"phone_number": phone_number})
    except Exception as e:
        logger.error("##### EXCEPTION IN FIND_EXIST_USER FUNCTION IS {}".format(e))
    finally:
        logger.info("##### METHOD OVER ####")


def find_slug_therapist(slug: str):
    try:
        query = "SELECT * FROM doctors where slug=:slug"
        logger.info("######## PROCEEDING FURTHER FOR THE EXECUTION OF SLUG QUERY #########")
        return db.fetch_one(query=query, values={"slug": slug})
    except Exception as e:
        logger.error("##### EXCEPTION IN FIND_SLUG_THERAPIST FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND IND_SLUG_THERAPIST FUNCTION COMPLETED ####")


def save_doctor(doctor: Doctor, slug):
    dt = datetime.now(timezone.utc)
    try:
        query = """ INSERT INTO doctors VALUES (nextval('doctors_id_seq'),:username,:full_name,:mail,:password,:phone_number,:gender,:experience,:econsultation_fee,:isActive,:isOnline,:url,:follow_up_fee,:about, :slug, :created_on) RETURNING id """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.execute(query=query, values={"username": doctor.username,
                                               "full_name": doctor.full_name, "mail": doctor.mail,
                                               "password": doctor.password,
                                               "phone_number": doctor.phone_number, "gender": doctor.gender,
                                               "experience": doctor.experience,
                                               "econsultation_fee": doctor.econsultation_fee,
                                               "isActive": doctor.isActive,
                                               "isOnline": doctor.isActive,
                                               "url": doctor.url,
                                               "follow_up_fee": doctor.follow_up_fee,
                                               "about": doctor.about,
                                               "slug": slug,
                                               "created_on": dt.utcnow()
                                               }
                          )

    except Exception as e:
        logger.error(
            "##### EXCEPTION IN SAVE_DOCTOR FUNCTION IS {}, FOR THE THERAPIST {} ####".format(e, doctor.mail))
        return {"mail": doctor.mail, "message": "cannot able to add in db", "code": 400}
    finally:
        logger.info("#### save_user FUNCTION COMPLETED ####")


def save_specialisation_map(map):
    query = "INSERT INTO doctors_specialisations_map VALUES (nextval('doctors_specialisations_map_id_seq'),:doctor_id,:specialisation_id) "
    logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF SAVE SPECIALISATION MAP QUERY")
    try:
        return db.execute_many(query=query, values=map)
    except Exception as e:
        logger.error("####### EXCEPTION IN SAVE_SPECIALISATION_MAP FUNCTION IS = {}".format(e))
        return False
    finally:
        logger.error("#######  SAVE_SPECIALISATION_MAP FUNCTION OVER ##### ")


def save_languages_map(map):
    query = "INSERT INTO doctors_languages_map VALUES (nextval('doctors_languages_map_id_seq'),:doctor_id,:languages_id,now() at time zone 'UTC') "
    logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF SAVE LANGUAGES MAP QUERY")
    try:
        return db.execute_many(query=query, values=map)
    except Exception as e:
        logger.error("####### EXCEPTION IN SAVE_LANGUAGES_MAP FUNCTION IS = {}".format(e))
        return False
    finally:
        logger.error("#######  SAVE_LANGUAGES_MAP FUNCTION OVER ##### ")


def find_specialisation(specialisation_value: int):
    query = "SELECT name FROM SPECIALISATIONS WHERE id=:id"
    logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF FIND SPECIALISATION QUERY")
    try:
        return db.fetch_one(query=query, values={"id": specialisation_value})
    except Exception as e:
        logger.error("###### ERROR IN FINDING SPECIALISATION FROM THE DATABASE {} ######".format(e))


def find_black_list_token(token: str):
    query = "SELECT * FROM doctors_blacklists WHERE token=:token"
    try:
        return db.fetch_one(query, values={"token": token})
    except Exception as e:
        logger.error("####### EXCEPTION IN FIND_BLACK_LIST_TOKEN FUNCTION IS = {}".format(e))
    finally:
        logger.info("#### find_black_list_token FUNCTION COMPLETED ####")


def create_reset_code(mail: str, reset_code: str):
    try:
        query = """INSERT INTO doctors_codes VALUES (nextval('code_id_seq'),:mail,:reset_code,now() at time zone 'UTC',
        '1') """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.execute(query, values={"mail": mail, "reset_code": reset_code})
    except Exception as e:
        logger.error("##### EXCEPTION IN create_reset_code FUNCTION IS {}".format(e))
    finally:
        logger.info("#### create_reset_code FUNCTION COMPLETED ####")


def check_reset_password_token(reset_password_token: str):
    try:
        query = """SELECT * FROM doctors_codes WHERE status='1' AND reset_code=:reset_password_token AND expired_in >= now() AT TIME 
        ZONE 'UTC' - INTERVAL '10 minutes' """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.fetch_one(query, values={"reset_password_token": reset_password_token})
    except Exception as e:
        logger.error("##### EXCEPTION IN check_reset_password_token FUNCTION IS {}".format(e))
    finally:
        logger.info("#### check_reset_password_token FUNCTION COMPLETED ####")


def reset_password_user(new_hashed_password: str, mail: str):
    try:
        query = """ UPDATE doctors SET password=:password WHERE mail=:mail """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.execute(query, values={"password": new_hashed_password, "mail": mail})
    except Exception as e:
        logger.error("##### EXCEPTION IN reset_password_user FUNCTION IS {}".format(e))
    finally:
        logger.info("#### reset_password_user FUNCTION COMPLETED ####")


def disable_reset_code(reset_password_token: str, mail: str):
    query = "UPDATE doctors_codes SET status='9' WHERE status='1' AND reset_code=:reset_code AND mail=:mail"
    try:
        return db.execute(query, values={"reset_code": reset_password_token, "mail": mail})
    except Exception as e:
        logger.error("#### EXCEPTION IN DISABLE_RESET_CODE IS {}".format(e))
    finally:
        logger.info("#### disable_reset_password_user FUNCTION COMPLETED ####")


def get_doctor_information(mail: str):
    query = "SELECT id FROM doctors WHERE mail=:mail"
    try:
        return db.fetch_one(query, values={"mail": mail})
    except Exception as e:
        logger.error("####### EXCEPTION IN FIND_BLACK_LIST_TOKEN FUNCTION IS = {}".format(e))
    finally:
        logger.info("#### find_black_list_token FUNCTION COMPLETED ####")


def save_qualification(values):
    try:
        query = "INSERT INTO qualifications VALUES (nextval('qualifications_id_seq'),:doctor_id,:qualification_name," \
                ":institute_name,:year) "
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF SAVE QUALIFICATION QUERY")
        return db.execute_many(query=query, values=values)
    except Exception as e:
        logger.error("####### EXCEPTION IN SAVE_QUALIFICATION IS = {}".format(e))
        return {"error":
                    {"message": "error in save qualification",
                     "code": 400,
                     "success": False
                     }
                }
    finally:
        logger.info("#### SAVE_QUALIFICATION  FUNCTION COMPLETED ####")


def update_profile_picture(username, url):
    query = "UPDATE doctors SET url=:url WHERE username=:username "
    logger.info("####### UPDATING USER ##########")
    try:
        return db.execute(query=query, values={"username": username,
                                               "url": url
                                               })
    except Exception as e:
        logger.error("#### EXCEPTION IN UPDATE_USER FUNCTION IS {} FOR USER {}".format(e, username))
        return False
    finally:
        logger.info("##### UPDATE PROFILE PICTURE FUNCTION OVER ###### ")


def save_time_slot_config(val):
    try:
        query = " INSERT INTO doctors_time_slot VALUES (nextval('doctors_time_slot_id_seq'),:day,:video,:audio,:chat,:start_time,:end_time,:video_frequency,:audio_frequency,:chat_frequency,:is_available,:non_availability_reason,:is_active,now() at time zone 'UTC') RETURNING id; "
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF SAVE TIMESLOT QUERY")
        return db.execute(query=query, values={"day": val.day,
                                               "video": val.video,
                                               "audio": val.audio,
                                               "chat": val.chat,
                                               "start_time": val.start_time,
                                               "end_time": val.end_time,
                                               "video_frequency": val.video_frequency,
                                               "audio_frequency": val.audio_frequency,
                                               "chat_frequency": val.chat_frequency,
                                               "is_available": val.is_available,
                                               "non_availability_reason": val.non_availability_reason,
                                               "is_active": val.is_active
                                               })
    except Exception as e:
        logger.error("####### EXCEPTION IN SAVE_TIME_SLOT IS = {}".format(e))
        return {"error":
                    {"message": "error in time slot configuration",
                     "code": 400,
                     "success": False
                     }
                }
    finally:
        logger.info("#### TIMESLOT CONFIGURATION  FUNCTION COMPLETED ####")


def save_timeSlot_doctor_map(map_array_object):
    try:
        logger.info("##### GOING FOR SAVING TIME_SLOT AND DOCTOR_ID QUERY ####### ")
        query = "INSERT INTO doctors_timeSlot_map VALUES (nextval('doctors_timeSlot_map_id_seq'),:doctor_id,:time_slot_id,now() at time zone 'UTC')"
        return db.execute_many(query, values=map_array_object)
    except Exception as e:
        logger.error("##### EXCEPTION IN TIME_SLOT AND DOCTOR_ID MAP QUERY {} #########".format(e))
        return {"error": {"message": "error occured due to {}".format(e),
                          "code": 400,
                          "success": False
                          }}
    finally:
        logger.info("#### SAVING TIME_SLOT AND DOCTOR_ID OVER ######")


def get_doctor_id(slug: str):
    query = "SELECT id FROM doctors WHERE slug=:slug"
    try:
        return db.fetch_one(query, values={"slug": slug})
    except Exception as e:
        logger.error("####### EXCEPTION IN FIND_ID FROM DOCTORS TABLE FUNCTION IS = {}".format(e))
    finally:
        logger.info("#### get_doctor_id FUNCTION COMPLETED ####")


def find_doctor_information(slug: str):
    query = "SELECT * FROM doctors WHERE slug=:slug"
    try:
        return db.fetch_one(query, values={"slug": slug})
    except Exception as e:
        logger.error("####### EXCEPTION IN FIND_DOCTOR_INFORMATION FROM DOCTORS TABLE FUNCTION IS = {}".format(e))
    finally:
        logger.info("#### get_doctor_id FUNCTION COMPLETED ####")


def find_time_slot(doctor_id: int):
    query = """SELECT day,video,audio,chat,start_time,end_time,video_frequency,audio_frequency,chat_frequency, 
    doctor_id FROM doctors_time_slot,doctors_timeslot_map WHERE 
    doctors_time_slot.id=doctors_timeslot_map.time_slot_id AND doctor_id=:doctor_id AND is_available='true' AND 
    start_time>now() at time zone 'UTC' ORDER BY start_time"""
    try:
        return db.fetch_all(query, values={"doctor_id": doctor_id})
    except Exception as e:
        logger.error("####### EXCEPTION IN FIND_DOCTOR_INFORMATION FROM DOCTORS TABLE FUNCTION IS = {}".format(e))
    finally:
        logger.info("#### get_doctor_id FUNCTION COMPLETED ####")


def get_time_slot_configuration(doctor_id: int):
    query = """SELECT day,video,audio,chat,start_time,end_time,video_frequency,audio_frequency,chat_frequency,is_available,non_availability_reason,is_active FROM doctors_time_slot,doctors_timeslot_map WHERE 
        doctors_time_slot.id=doctors_timeslot_map.time_slot_id AND doctor_id=:doctor_id """
    try:
        return db.fetch_all(query=query, values={"doctor_id": doctor_id})
    except Exception as e:
        logger.error("####### EXCEPTION IN ALL_TIME_SLOT_CONFIGURATION FROM DOCTORS TABLE FUNCTION IS = {}".format(e))
    finally:
        logger.info("#### ALL_TIME_SLOT_CONFIGURATION FUNCTION COMPLETED ####")


def find_booked_time_slot(doctor_id: int):
    query = """SELECT start_time,end_time,time_slot_config_id FROM consultations where doctor_id=:doctor_id"""
    try:
        return db.fetch_all(query=query, values={"doctor_id": doctor_id})
    except Exception as e:
        logger.error("####### EXCEPTION IN FIND_BOOKED_TIMESLOTS FROM CONSULTATION TABLE FUNCTION IS = {}".format(e))
    finally:
        logger.info("#### FIND_BOOKED_TIMESLOTS FUNCTION COMPLETED ####")


def check_if_language_id_exist(id: int):
    query = "SELECT * FROM languages WHERE id=:id"
    try:
        logger.info("### PROCEEDING FURTHER FOR EXECUTION OF QUERY OF GET SPECIFIC ID")
        return db.fetch_one(query, values={"id": id})
    except Exception as e:
        logger.error("error in fetching id {}".format(e))
    finally:
        logger.info("#### FIND ID METHOD OVER ######")


def update_language(id, name):
    query = "UPDATE languages SET name=:name WHERE id=:id RETURNING id"
    try:
        return db.execute(query, values={"name": name, "id": id})
    except Exception as e:
        logger.error("### ERROR IN UPDATING SPECIALISATION {} #####".format(e))
    finally:
        logger.info("##### UPDATE SPECIALISATION METHOD OVER ####")


def check_if_time_slot_id_exist(id):
    query = "SELECT * From doctors_time_slot WHERE id=:id"
    try:
        return db.fetch_one(query=query, values={"id": id})
    except Exception as e:
        logger.error("### ERROR IN FINDING TIMESLOT ID {} #####".format(e))
    finally:
        logger.info("##### FINDING TIMESLOT ID METHOD OVER ####")


def update_time_slot(query_object: str, update_value_map):
    try:
        return db.execute(query=query_object, values=update_value_map)
    except Exception as e:
        logger.error("### ERROR IN UPDATING SPECIALISATION {} #####".format(e))
    finally:
        logger.info("##### UPDATE SPECIALISATION METHOD OVER ####")


async def register_user_combined(doctor, slug):
    async with db.transaction():
        transaction = await db.transaction()
        try:
            dt = datetime.now(timezone.utc)
            logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
            doctor_id = await db.execute(query=QUERY_FOR_REGISTER_DOCTOR, values={"username": doctor.username,
                                                                                  "full_name": doctor.full_name,
                                                                                  "mail": doctor.mail,
                                                                                  "password": doctor.password,
                                                                                  "phone_number": doctor.phone_number,
                                                                                  "gender": doctor.gender,
                                                                                  "experience": doctor.experience,
                                                                                  "econsultation_fee": doctor.econsultation_fee,
                                                                                  "is_active": doctor.is_active,
                                                                                  "is_online": doctor.is_online,
                                                                                  "url": doctor.url,
                                                                                  "follow_up_fee": doctor.follow_up_fee,
                                                                                  "about": doctor.about,
                                                                                  "slug": slug,
                                                                                  "created_on": dt.utcnow()
                                                                                  }
                                         )
            logger.info("####### SUCCESS IN DOCTOR TABLE #########")
            map_object = []
            for get_index in doctor.specialisation:
                object_map = {"doctor_id": doctor_id,
                              "specialisation_id": get_index
                              }
                map_object.append(object_map)
            print(map_object)
            logger.info("####### GOING FOR EXECUTION OF DOCTOR SPECIALISATION MAP ########### ")
            await db.execute_many(query=QUERY_FOR_SPECIALISATION_MAP, values=map_object)
            logger.info("####### SUCCESSFULLY EXECUTED DOCTOR SPECIALISATION MAP ########### ")
            object_to_map = []
            for index in doctor.languages:
                to_map = {"doctor_id": doctor_id,
                          "languages_id": index
                          }
                object_to_map.append(to_map)
            logger.info("####### GOING FOR EXECUTION OF DOCTOR SAVE_LANGUAGE MAP ########### ")
            await db.execute_many(query=QUERY_FOR_SAVE_LANGUAGE, values=object_to_map)
            logger.info("####### SUCCESSFULLY EXECUTED LANGUAGE MAP ########### ")
            values = []
            for get_values in doctor.qualification:
                qualification_object = {"doctor_id": doctor_id,
                                        "qualification_name": get_values.qualification_name,
                                        "institute_name": get_values.institute_name,
                                        "year": get_values.year
                                        }
                values.append(qualification_object)
            logger.info("####### GOING GOR QUALIFICATION TABLE INSERTION ########## ")
            await db.execute_many(query=QUERY_FOR_SAVE_QUALIFICATION, values=values)
            logger.info("####### SUCCESSFULLY EXECUTED SAVE_QUALIFICATION MAP ########### ")
        except Exception as WHY:
            logger.error("######### ERROR IN THE QUERY BECAUSE {} ".format(WHY))
            logger.info("########## ROLLING BACK TRANSACTIONS #################")
            await transaction.rollback()
            return False
        else:
            logger.info("##### ALL WENT WELL COMMITTING TRANSACTION ########")
            await transaction.commit()
            logger.info("###### TRANSACTION COMMITTED AND SUCCESS TRUE #######")
            return True


def find_particular_specialisation(name):
    try:
        query = "SELECT * FROM specialisations WHERE name=:name"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF FINDING PARTICULAR ####")
        return db.fetch_one(query=query, values={"name": name})
    except Exception as e:
        logger.error("##### EXCEPTION IN SAVE_LANGUAGE FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND PARTICULAR_LANGUAGE FUNCTION COMPLETED ####")
