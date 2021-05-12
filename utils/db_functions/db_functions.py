from models.doctor import Doctor
from utils.logger.logger import logger
from utils.connection_configuration.db_object import db
from datetime import datetime, timezone
from models.specialisation import Specialisation


def save_specialisation(specailisations: Specialisation):
    try:
        query = """INSERT INTO specialisations VALUES (nextval('specialisations_id_seq'),:name,:active) """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF SPECIALISATION")
        return db.execute(query, values={"name": specailisations.name,
                                         "active": specailisations.active})
    except Exception as e:
        logger.error("##### EXCEPTION IN SAVE_SPECIALISATION FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### FIND SAVE_SPECIALISATION FUNCTION COMPLETED ####")


def get_sepecific_specialisation(search_query: str):
    try:
        query = "select * from specialisations where active=:active"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET SPECIALISATION")
        return db.fetch_all(query, values={"active": search_query})
    except Exception as e:
        print(e)
        logger.error("##### EXCEPTION IN GET_SPECIALISATION FUNCTION IS {}".format(e))
        return False
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
    print("one")
    try:
        query = """ INSERT INTO doctors VALUES (nextval('doctors_id_seq'),:username,:full_name,:mail,:password," \
                ":phone_number,:gender,:experience,:econsultation_fee,:isActive,:isOnline,:slug,:url,:created_on," \
                ":follow_up_fee,:about) """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.execute(query=query, values={"username": doctor.username,
                                               "full_name": doctor.full_name, "mail": doctor.mail,
                                               "password": doctor.password,
                                               "phone_number": doctor.phone_number, "gender": doctor.gender,
                                               "experience": doctor.experience,
                                               "econsultation_fee": doctor.econsultation_fee,
                                               "isActive": doctor.isActive,
                                               "isOnline": doctor.isActive,
                                               "slug": slug,
                                               "created_on": dt.utcnow(),
                                               "follow_up_fee": doctor.follow_up_fee,
                                               "about": doctor.about
                                               }
                          )

    except Exception as e:
        logger.error(
            "##### EXCEPTION IN SAVE_DOCTOR FUNCTION IS {}, FOR THE THERAPIST {} ####".format(e, doctor.mail))
        return {"mail": doctor.mail, "message": "cannot able to add in db", "code": 400}
    finally:
        logger.info("#### save_user FUNCTION COMPLETED ####")


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


def get_doctor_information(username: str):
    query = "SELECT id FROM doctors WHERE username=:username"
    try:
        return db.fetch_one(query, values={"username": username})
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
