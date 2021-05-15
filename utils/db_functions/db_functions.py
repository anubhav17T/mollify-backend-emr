from models.doctor import Doctor
from utils.logger.logger import logger
from utils.connection_configuration.db_object import db
from datetime import datetime, timezone
from models.specialisation import Specialisation
from models.doctor_specialisation import DoctorSpecialisation
from models.time_slot_configuration import TimeSlot


def save_specialisation(specailisations: Specialisation):
    try:
        query = """INSERT INTO specialisations VALUES (nextval('specialisations_id_seq'),:name,:is_active) """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF SPECIALISATION")
        return db.execute(query, values={"name": specailisations.name,
                                         "is_active": "true"})
    except Exception as e:
        logger.error("##### EXCEPTION IN SAVE_SPECIALISATION FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### FIND SAVE_SPECIALISATION FUNCTION COMPLETED ####")


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


def get_sepecific_specialisation(state: str):
    try:
        query = "select * from specialisations where is_active=:is_active"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET SPECIALISATION")
        return db.fetch_all(query, values={"is_active": state})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_SPECIALISATION FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_SPECIALISATION FUNCTION COMPLETED ####")


def get_all_specialisation():
    try:
        query = "select * FROM specialisations"""
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
        query = """ INSERT INTO doctors VALUES (nextval('doctors_id_seq'),:username,:full_name,:mail,:password,:phone_number,:gender,:experience,:econsultation_fee,:isActive,:isOnline,:url,:follow_up_fee,:about, :slug, :created_on) """
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
        query = " INSERT INTO doctors_time_slot VALUES (nextval('doctors_time_slot_id_seq'),:day,:video,:audio,:chat,:start_time,:end_time,:video_frequency,:audio_frequency,:chat_frequency,:is_available,:non_availability_reason,:is_active) RETURNING id; "
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


def save_timeSlot_doctor_map(doctor_id, time_slot_id):
    try:
        logger.info("##### GOING FOR SAVING TIME_SLOT AND DOCTOR_ID QUERY ####### ")
        query = "INSERT INTO doctors_timeSlot_map VALUES (nextval('doctors_timeSlot_map_id_seq'),:doctor_id,:time_slot_id) RETURNING id"
        return db.execute(query, values={"doctor_id": doctor_id, "time_slot_id": time_slot_id})
    except Exception as e:
        logger.error("##### EXCEPTION IN TIME_SLOT AND DOCTOR_ID MAP QUERY {} #########".format(e))
        return {"error": {"message": "error occured due to {}".format(e),
                          "code": 400,
                          "success": False
                          }}
    finally:
        logger.info("#### SAVING TIME_SLOT AND DOCTOR_ID OVER ######")