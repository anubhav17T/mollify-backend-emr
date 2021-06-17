from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.v1.doctor_language_routes import doctor_languages
from routes.v1.doctor_specialisation_routes import doctor_specialisation
from routes.v1.doctors_qualification_routes import doctor_qualification_router
from routes.v2.doctor_filter_routes import app_v2_filters
from utils.custom_exceptions.custom_exceptions import CustomException, \
    CustomExceptionHandler
from utils.connection_configuration.check_connection import DatabaseConfiguration
from utils.connection_configuration.db_object import db
from utils.tables.db_tables import creating_doctor_table, creating_blacklist_table, creating_codes_table, \
    creating_qualification_table, creating_specialisations_table, doctor_specialisation_mapping, doctors_time_slot, \
    doctors_timeSlot_map, feedback, consultation, creating_language_table, doctor_language_mapping
from utils.logger.logger import logger
from routes.v1.v1 import app_v1
from routes.v1.doctor_routes import doctor_routes
from routes.v1.doctor_time_slot_routes import doctor_time_slot_routes
from routes.v1.doctor_feedback_routes import doctor_feedback
from routes.v1.doctor_consultation_routes import doctor_consultation

origins = ["*"]
conn = DatabaseConfiguration()


def connections():
    conn.checking_database_connection()
    creating_doctor_table()
    creating_qualification_table()
    creating_specialisations_table()
    creating_blacklist_table()
    creating_codes_table()
    doctor_specialisation_mapping()
    doctors_time_slot()
    doctors_timeSlot_map()
    consultation()
    feedback()
    creating_language_table()
    doctor_language_mapping()


connections()

app = FastAPI(title="Mollify RestApi's Version 1.0",
              description="Api For EMR Service, Developer=Anubhav Tyagi(anubhav1tyagi@gmail.com)",
              version="1.0.0"
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_v1, prefix="/api/v1")
app.include_router(doctor_routes, prefix="/api/v1")
app.include_router(doctor_time_slot_routes, prefix="/api/v1")
app.include_router(doctor_feedback, prefix="/api/v1")
app.include_router(doctor_consultation, prefix="/api/v1")
app.include_router(doctor_specialisation, prefix="/api/v1")
app.include_router(doctor_languages, prefix="/api/v1")
app.include_router(doctor_qualification_router, prefix="/api/v2")
app.include_router(app_v2_filters, prefix="/api/v2")


@app.get("/")
async def home():
    return {"API": "MOLLIFY DOCTOR-EMR SERVICE"}


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.exception_handler(CustomException)
async def unicorn_exception_handler(request: Request, e: CustomException):
    return JSONResponse(
        status_code=e.status_code,
        content={"code": e.status_code, "message": e.detail}
    )


@app.exception_handler(CustomExceptionHandler)
async def NotFoundException(request: Request, exception: CustomExceptionHandler):
    return JSONResponse(status_code=exception.code,
                        content={"error": {"message": exception.message,
                                           "code": exception.code,
                                           "target": exception.target,
                                           "success": exception.success
                                           }
                                 })


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response
#
#
# if __name__ == "__main__":
#     try:
#         """ADD MULTIPLE PROCESSING IN CREATING DATABASE TABLE FOR FAST EXECUTION """
#         import uvicorn
#
#         uvicorn.run(app)
#     except Exception as e:
#         logger.error("###### EXCEPTION IN MAIN FILE IS {} ####### ".format(e))
