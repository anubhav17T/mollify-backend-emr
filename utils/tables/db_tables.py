from constants.const import DB_URL, DB_PORT, DB_NAME, DB_USER, DB_HOST, DB_PASSWORD
import sqlalchemy
from sqlalchemy import DateTime, Integer, Sequence, ARRAY
from utils.logger.logger import logger
import psycopg2
from sqlalchemy import ForeignKey
from sqlalchemy_utils import URLType


def creating_doctor_table():
    try:
        logger.info(" ########## GOING FOR DOCTOR/THERAPIST TABLES ##############")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('doctor',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            logger.info("####### DOCTOR/THERAPIST TABLE DOESN'T EXIST ########")
            metadata = sqlalchemy.MetaData()
            doctor = sqlalchemy.Table(
                "doctors",
                metadata,
                sqlalchemy.Column("id", Integer, Sequence("doctors_id_seq"), primary_key=True),
                sqlalchemy.Column("username", sqlalchemy.String()),
                sqlalchemy.Column("full_name", sqlalchemy.String()),
                sqlalchemy.Column("mail", sqlalchemy.String()),
                sqlalchemy.Column("password", sqlalchemy.String()),
                sqlalchemy.Column("phone_number", sqlalchemy.String()),
                sqlalchemy.Column("gender", sqlalchemy.String()),
                sqlalchemy.Column("experience", sqlalchemy.String()),
                sqlalchemy.Column("econsultation_fee", sqlalchemy.Integer),
                sqlalchemy.Column("is_active", sqlalchemy.Boolean()),
                sqlalchemy.Column("is_online", sqlalchemy.Boolean()),
                sqlalchemy.Column("url", sqlalchemy.String(150)),
                sqlalchemy.Column("follow_up_fee", sqlalchemy.Integer),
                sqlalchemy.Column("about", sqlalchemy.String(300)),
                sqlalchemy.Column("slug", sqlalchemy.String(150)),
                sqlalchemy.Column("created_on", DateTime),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return doctor
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING THERAPIST TABLE {} ########".format(e))


def creating_qualification_table():
    try:
        logger.info("######## GOING FOR QUALIFICATION TABLE #########")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('qualifications',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABSE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            qualifications = sqlalchemy.Table(
                "qualifications", metadata,
                sqlalchemy.Column("id", Integer, Sequence("qualifications_id_seq"), primary_key=True),
                sqlalchemy.Column("doctor_id", Integer),
                sqlalchemy.Column("qualification_name", sqlalchemy.String(100)),
                sqlalchemy.Column("institute_name", sqlalchemy.String(100)),
                sqlalchemy.Column("year", sqlalchemy.String(100)),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return qualifications
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING QUALIFICATION TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE QUALIFICATION TABLE FUNCTION OVER ###### ")


def creating_blacklist_table():
    try:
        logger.info(" ########## GOING FOR BLACKLIST TABLES ##############")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('doctors_blacklists',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABSE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            blacklists = sqlalchemy.Table(
                "doctors_blacklists", metadata,
                sqlalchemy.Column("token", sqlalchemy.String(250), unique=True),
                sqlalchemy.Column("mail", sqlalchemy.String(100))
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3, max_overflow=0)
            metadata.create_all(engine)
            conn.close()
            return blacklists
    except Exception as e:
        logger.error("{}".format(e))


def creating_codes_table():
    try:
        logger.info(" ########## GOING FOR CODES TABLES ##############")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('doctors_codes',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABSE PASSING IT")
            conn.close()
            return True
        else:
            logger.info("#### CODES TABLE DOESN'T EXIST #### ")
            metadata = sqlalchemy.MetaData()
            codes = sqlalchemy.Table(
                "doctors_codes",
                metadata,
                sqlalchemy.Column("id", Integer, Sequence("code_id_seq"), primary_key=True),
                sqlalchemy.Column("mail", sqlalchemy.String(100)),
                sqlalchemy.Column("reset_code", sqlalchemy.String(60)),
                sqlalchemy.Column("expired_in", DateTime),
                sqlalchemy.Column("status", sqlalchemy.String(1))
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3, max_overflow=0)
            metadata.create_all(engine)
            conn.close()
            return codes
    except Exception as e:
        logger.error("{}".format(e))


def creating_specialisations_table():
    try:
        logger.info("######## GOING FOR SPECIALISATION TABLE #########")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('specialisations',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            specialisations = sqlalchemy.Table(
                "specialisations", metadata,
                sqlalchemy.Column("id", Integer, Sequence("specialisations_id_seq"), primary_key=True),
                sqlalchemy.Column("name", sqlalchemy.String(100)),
                sqlalchemy.Column("is_active", sqlalchemy.Boolean),
                sqlalchemy.Column("created_on", DateTime),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return specialisations
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING SPECIALISATION TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE SPECIALISATION TABLE FUNCTION OVER ###### ")


def doctor_specialisation_mapping():
    logger.info("######## GOING FOR SPECIALISATION TABLE #########")
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('doctors_specialisation_map',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            doctors_specialisations_map = sqlalchemy.Table(
                "doctors_specialisations_map", metadata,
                sqlalchemy.Column("id", Integer, Sequence("doctors_specialisations_map_id_seq"), primary_key=True),
                sqlalchemy.Column("doctor_id", Integer),
                sqlalchemy.Column("specialisation_id", Integer),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return doctors_specialisations_map
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING SPECIALISATION TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE SPECIALISATION TABLE FUNCTION OVER ###### ")


def doctors_time_slot():
    logger.info("######## GOING FOR DOCTOR TIME-SLOT-CONFIG TABLE #########")
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('doctors_time_slot',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            doctors_time_slot = sqlalchemy.Table(
                "doctors_time_slot", metadata,
                sqlalchemy.Column("id", Integer, Sequence("doctors_time_slot_id_seq"), primary_key=True),
                sqlalchemy.Column("day", sqlalchemy.String(10)),
                sqlalchemy.Column("video", sqlalchemy.Boolean),
                sqlalchemy.Column("audio", sqlalchemy.Boolean),
                sqlalchemy.Column("chat", sqlalchemy.Boolean),
                sqlalchemy.Column("start_time", DateTime),
                sqlalchemy.Column("end_time", DateTime),
                sqlalchemy.Column("video_frequency", Integer),
                sqlalchemy.Column("audio_frequency", Integer),
                sqlalchemy.Column("chat_frequency", Integer),
                sqlalchemy.Column("is_available", sqlalchemy.Boolean),
                sqlalchemy.Column("non_availability_reason", sqlalchemy.String(300)),
                sqlalchemy.Column("is_active", sqlalchemy.Boolean),
                sqlalchemy.Column("buffer_time", sqlalchemy.Integer),
            sqlalchemy.Column("created_on", DateTime),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return doctors_time_slot
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING SPECIALISATION TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE DOCTOR-TIME-SLOT TABLE FUNCTION OVER ###### ")


def doctors_timeSlot_map():
    logger.info("######## GOING FOR TIMESLOT DOCTORID MAP TABLE #########")
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('doctors_timeSlot_map',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            doctors_timeslot_map = sqlalchemy.Table(
                "doctors_timeslot_map", metadata,
                sqlalchemy.Column("id", Integer, Sequence("doctors_timeslot_map_id_seq"), primary_key=True),
                sqlalchemy.Column("doctor_id", Integer),
                sqlalchemy.Column("time_slot_id", Integer),
                sqlalchemy.Column("created_on", DateTime),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return doctors_timeslot_map
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING SPECIALISATION TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE SPECIALISATION TABLE FUNCTION OVER ###### ")


def feedback():
    logger.info("######## GOING FOR DOCTOR/THERAPIST FEEDBACK  TABLE #########")
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('feedbacks',))
        if bool(cur.rowcount):
            logger.info("#### TABLE FEEDBACK ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            feedbacks_table = sqlalchemy.Table(
                "feedbacks", metadata,
                sqlalchemy.Column("id", Integer, Sequence("feedbacks_id_seq"), primary_key=True),
                sqlalchemy.Column("consultation_id", Integer),
                sqlalchemy.Column("doctor_id", Integer),
                sqlalchemy.Column("rating", sqlalchemy.FLOAT),
                sqlalchemy.Column("description", sqlalchemy.String(300)),
                sqlalchemy.Column("patient_id", Integer),
                sqlalchemy.Column("created_on", DateTime),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return feedbacks_table
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING FEEDBACK TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE FEEDBACK TABLE FUNCTION OVER ###### ")


def consultation():
    """:returns consultation table"""
    logger.info("######## GOING FOR DOCTOR/THERAPIST CONSULTATION  TABLE #########")
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('consultations',))
        if bool(cur.rowcount):
            logger.info("#### TABLE CONSULTATIONS ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            consultations_table = sqlalchemy.Table(
                "consultations", metadata,
                sqlalchemy.Column("id", Integer, Sequence("consultations_id_seq"), primary_key=True),
                sqlalchemy.Column("patient_id", Integer),
                sqlalchemy.Column("doctor_id", Integer),
                sqlalchemy.Column("parent_id", Integer),
                sqlalchemy.Column("start_time", DateTime),
                sqlalchemy.Column("end_time", DateTime),
                sqlalchemy.Column("time_slot_config_id", Integer),
                sqlalchemy.Column("status", sqlalchemy.String(10)),
                sqlalchemy.Column("cancel_reason", sqlalchemy.String(200)),
                sqlalchemy.Column("created_on", DateTime),
                sqlalchemy.Column("day",sqlalchemy.String(10))
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return consultations_table
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING CONSULTATIONS TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE CONSULTATIONS TABLE FUNCTION OVER ###### ")


def creating_language_table():
    try:
        logger.info("######## GOING FOR LANGUAGE TABLE #########")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('languages',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            languages = sqlalchemy.Table(
                "languages", metadata,
                sqlalchemy.Column("id", Integer, Sequence("languages_id_seq"), primary_key=True),
                sqlalchemy.Column("name", sqlalchemy.String(100)),
                sqlalchemy.Column("is_active", sqlalchemy.Boolean),
                sqlalchemy.Column("created_on", DateTime),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return languages
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING LANGUAGES TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE LANGUAGES TABLE FUNCTION OVER ###### ")


def doctor_language_mapping():
    logger.info("######## GOING FOR DOCTOR-LANGUAGE-MAP TABLE #########")
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('doctors_languages_map',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            doctors_languages_map = sqlalchemy.Table(
                "doctors_languages_map", metadata,
                sqlalchemy.Column("id", Integer, Sequence("doctors_languages_map_id_seq"), primary_key=True),
                sqlalchemy.Column("doctor_id", Integer),
                sqlalchemy.Column("languages_id", Integer),
                sqlalchemy.Column("created_on", DateTime),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return doctors_languages_map
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING SPECIALISATION TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE SPECIALISATION TABLE FUNCTION OVER ###### ")

# 2021-05-15 20:20:00
