""" API DESIGN FOR FILTRATION """
from fastapi import APIRouter, Query, Depends
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.paginator import paginate
from fastapi import status
from typing import List

from models.doctor import Doctor, DoctorOut
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_functions import get_all_doctor, get_sepecific_specialisation, get_doctor_on_specialisation, \
    filter_doctor, get_doctor_on_languages
from utils.helper_function.misc import list_to_set_with_case_conversion
from utils.logger.logger import logger

app_v2_filters = APIRouter()


# todo: Need to add rating support and pagination for this route

@app_v2_filters.get("/doctors/explore/", tags=["DOCTORS/FILTERS"],
                    response_model=Page[DoctorOut],
                    description="Get Specific Specialisation by name")
async def get_specific_specialisation(expertise: List[str] = Query(None, title="Query parameter for finding specific "
                                                                               "specialisation"),
                                      language: List[str] = Query(None, title="Query parameter for finding specific "
                                                                              "specialisation")):
    if expertise is None and language is None:
        return await get_all_doctor()


    else:
        languages = list_to_set_with_case_conversion(language, 2)
        expertises = list_to_set_with_case_conversion(expertise, 1)
        if expertises is None:
            response = await get_doctor_on_languages(languages)
        elif languages is None:
            response = await get_doctor_on_specialisation(expertises)
        else:
            response = await filter_doctor(expertises, languages)
        # TODO: write a logic such that when languages and speciality both selected the only common therapists lists returned
        if not response:
            logger.error("########### NO DOCTOR FOUND FOR GIVEN NAME ############")
            raise CustomExceptionHandler(message="We regret we are not able to find the doctor.Please try again later.",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         success=False,
                                         target="GET-SPECIFIC-DOCTOR")
        else:
            logger.info("##### FOUND THE THERAPISTS ######")
            return paginate(response)

add_pagination(app_v2_filters)
