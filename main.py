from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.custom_exceptions.custom_exceptions import CustomException
from utils.connection_configuration.check_connection import DatabaseConfiguration
from utils.connection_configuration.db_object import db
from utils.tables.db_tables import creating_doctor_table, creating_blacklist_table, creating_codes_table, \
    creating_qualification_table, creating_specialisations_table, doctor_specialisation_mapping, doctors_time_slot, \
    doctors_timeSlot_map
from utils.logger.logger import logger
from routes.v1 import app_v1
from routes.doctor_routes import doctor_routes
from routes.doctor_time_slot_routes import doctor_time_slot_routes

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


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response


if __name__ == "__main__":
    try:
        """ADD MULTIPLE PROCESSING IN CREATING DATABASE TABLE FOR FAST EXECUTION """
        connections()
    except Exception as e:
        logger.error("###### EXCEPTION IN MAIN FILE IS {} ####### ".format(e))
