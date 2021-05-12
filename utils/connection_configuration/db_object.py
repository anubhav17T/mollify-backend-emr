from constants.const import DB_URL
from databases import Database
from utils.logger.logger import logger
try:
    logger.info(" ########## GOING FOR CONNECTION ##############")
    db = Database(DB_URL)
except Exception as e:
    logger.error("###### EXCEPTION IN DB_OBJECT IS {} ###########".format(e))
