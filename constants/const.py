""" USER MODEL CONSTANTS """
NAME_DESC = "Provides the name of the user"
TITLE_DESC = "Name of the user"
PASSWORD_DESC = "Password of the user"
EMAIL_REGEX = "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
PHONE_REGEX = "(0/91)?[7-9][0-9]{9}"

""" ============= DATABASE CONFIGURATION FILE ================== """
# postgres password = postgres
# DB_HOST = "localhost"
# DB_USER = "postgres"
# DB_PASSWORD = "mollify@123"
# DB_NAME = "mollify"
# DB_PORT = 5432
# DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

""" =================== CLOUDINARY CONFIGURATION        ===================== """

CLOUD_NAME = "mollify"
API_KEY = "466423759736745"
API_SECRET = "Arv-iXxAZuNrVgf3k4_nS47VFag"
#
DB_HOST = "ec2-54-163-254-204.compute-1.amazonaws.com"
DB_USER = "jkyfmagnmgcpjs"
DB_PASSWORD = "a63ffcd21fa58bf0619dd063e87da51afa3b665b4c1305ea73014dbad828f59e"
DB_NAME = "d42op193oij6q"
DB_PORT = 5432
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


""" ============= JWT TOKEN =================="""
JWT_SECRET_KEY = "ef0a1569207bcb280212eb1a0e5948fed64f948049b531574c95813edd8c745c"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME = 80 * 24 * 5
MAIN_PAGE_DESCRIPTION = "For the main page of the application"
MAIN_PAGE_SUMMARY = "It returns the main page"

"""================== SECURITY CONSTANTS  ==============="""
BCRYPT_SCHEMA = "bcrypt"

""" =============== EMAIL CONFIGURATIONS ========"""
MAIL_USERNAME = "",
MAIL_PASSWORD = "",
MAIL_FROM = "",
MAIL_PORT = 587,
MAIL_SERVER = "smtp.gmail.com",
MAIL_TLS = True,
MAIL_SSL = False,
USE_CREDENTIALS = True

""" =============== REDIS CONFIGURATIONS ============ """
REDIS_URL = "redis://localhost"
REDIS_URL_PRODUCTION = "redis://167.71.12.16"

""" ======== EMAIL CONFIGURATOIN ============= """

REGISTRATION_BODY = """<html>
    <head></head>
    <body>
      <h1>WELCOME ON BOARD, REGISTRATION SUCCESSFULL</h1>
      <p>You have been registerd, thank you for choosing us
    </body>
    </html> """

FORGOT_PASSWORD_BODY = """<html>
    <head></head>
    <body>
      <h1>You have requested for reset password</h1>
      {}
      <p>Please see the instructions to reset your password
    </body>
    </html> """

""" ============== MISCELLANEOUS ============="""

TESTING = False
IS_LOAD_TEST = False
# IS_PRODUCTION = True if os.environ["PRODUCTION"] == "true" else False


"========== CONFERENCING ========== "
APPLICATION_ID = "72e966f174b748bca6a35e5b281d7c9d"
APPLICATION_CERTIFICATE = "f04e1c68506c4d309deb06ffff8e0088"

"============== ALEMBIC LOCAL CONFIGURATION =========="
URL = "postgresql://postgres:mollify@123@localhost/mollify"


SENDGRID_API_KEY = "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"


""" QUERIES FOR UPDATE TIMESLOTS """
UPDATE = "UPDATE doctors_time_slot SET "
WHERE = " WHERE id=:id Returning id"


""" STRING FUNCTIONS """
ADDING_YEARS = "+" +" years"

""" V1 PREFIX """

V1_PREFIX = "/api/v1"
V2_PREFIX = "/api/v2"


AWS_ACCESS_KEY = "AKIAQXR2EI3CXO3QVUF5"
AWS_SECRET_KEY = "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"


TIME_SLOT_ID_KEY = "time_slot_id"

DOCTOR_ID_KEY = "doctor_id"
