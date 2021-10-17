import json

from fastapi import APIRouter
from starlette import status
from models.client_documents.therapy_plan import TherapyPlan
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.logger.logger import logger
import requests

documents = APIRouter()
# URL = "https://mollify-backend-emr-micro.herokuapp.com/api/v1/user/document/therapy-plan/"
URL = "http://localhost:8001/v1/user/document/therapy-plan"


@documents.post("/user/document/therapy-plan/{id}", description="THERAPY PLAN FOR THE USER", tags=["DOCUMENTS/USER"])
async def user_therapy_plan(plan: TherapyPlan, id: int):
    logger.info("###### ADDING THERAPY PLAN DOCUMENT #########")
    if plan.document_type.name.upper() != "THERAPY_PLAN":
        logger.error("###### ERROR IN DOCUMENT TYPE #########")
        raise CustomExceptionHandler(message="Something went wrong,cannot save therapy plan.",
                                     code=status.HTTP_417_EXPECTATION_FAILED,
                                     success=False,
                                     target="document should be THERAPY_PLAN"
                                     )
    try:
        print(URL + "{}".format(id))
        data = {"consultation_id":plan.consultation_id,"document_type":plan.document_type.name,"therapy_plan_html":plan.therapy_plan_html}
        response = requests.post(URL,data=data)
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
        else:
            raise CustomExceptionHandler(message="Something went wrong at our end,Broken Pipeline",
                                         success=False,
                                         code=response.status_code,
                                         target="USER THERAPY PLAN"
                                         )
    except Exception as Why:
        raise CustomExceptionHandler(message="Something went wrong at our end,Broken Pipeline",
                                     success=False,
                                     code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     target="USER THERAPY PLAN {}".format(Why)
                                     )
    return data
