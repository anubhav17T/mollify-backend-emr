from fastapi import Request, Path, Query
import re
from fastapi import status, APIRouter, HTTPException, Depends
from models.specialisation import Specialisation, SpecialisationUpdate
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_functions import save_specialisation, get_true_specialisation, get_false_specialisation, \
    get_all_specialisation, find_particular_specialisation
from utils.db_functions.db_specialisation_function import check_if_id_exists, update_specialisation, \
    update_specialisation_table, get_specialisation_of_doctor
from utils.logger.logger import logger
from utils.utils_classes.classes_for_checks import CheckUserExistence

doctor_specialisation = APIRouter()


@doctor_specialisation.post("/doctors/specialisations", tags=["DOCTORS/SPECIALISATIONS"],
                            description="Create specialisation")
async def adding_specialisation(specailisation: Specialisation):
    logger.info("###### ADDING SPECIALISATION ######## ")
    if specailisation.name is None:
        raise CustomExceptionHandler(message="Specialisation value not provided",
                                     code=status.HTTP_400_BAD_REQUEST, success=False, target="Post Specialisation")
    check_response = await find_particular_specialisation(name=specailisation.name)
    if check_response is not None:
        raise CustomExceptionHandler(message="Specialisation already added",
                                     code=status.HTTP_409_CONFLICT,
                                     success=False,
                                     target="Post Specialisation")
    try:
        await save_specialisation(specailisation)
        return {"message": "specialisation added successfully", "code": status.HTTP_201_CREATED, "success": True}
    except Exception as e:
        logger.error("###### ERROR IN ADDING SPECIALISATION {} ###########".format(e))
        return {"error": {
            "message": "Unable to save specialisation {}".format(e),
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "target": "SAVE-SPECIALISATION"
        }}
    finally:
        logger.info("#### REGISTER SPECIALISATION FUNCTION OVER #####")


@doctor_specialisation.patch("/doctors/specialisations/{specialisation_id}", tags=["DOCTORS/SPECIALISATIONS"],
                             description="Update specialisation")
async def update_specialisation_name(specialisation: Specialisation,
                                     specialisation_id: int = Path(..., description="Should be passed as integer")):
    response = CheckUserExistence(_id=specialisation_id, target="SPECIALISATION-PATCH")
    await response.check_specialisation_id_exist()

    check_resp = await update_specialisation(id=specialisation_id, name=specialisation.name)
    if not check_resp:
        return {"error": {"message": "cannot able to insert specialisation",
                          "code": status.HTTP_400_BAD_REQUEST,
                          "success": False
                          }
                }
    else:
        return {"message": "successfully updated the specialisation", "success": True, "code": status.HTTP_201_CREATED}


@doctor_specialisation.put("/doctors/specialisations/{specialisation_id}", tags=["DOCTORS/SPECIALISATIONS"],
                           description="Create specialisation")
async def update_specialisation_(specialisation_object: SpecialisationUpdate,
                                 specialisation_id: int = Path(..., description="Should be passed as integer")):
    logger.info("####### UPDATE SPECIALISATION TABLE METHOD IS CALLED ############")
    response = CheckUserExistence(_id=specialisation_id, target="SPECIALISATION-PATCH")
    await response.check_specialisation_id_exist()
    is_active = bool(specialisation_object.is_active)
    check_resp_id = await update_specialisation_table(var_id=specialisation_id,
                                                      name=specialisation_object.name,
                                                      is_active=is_active
                                                      )
    if not check_resp_id:
        return {"error": {"message": "cannot able to insert specialisation",
                          "code": status.HTTP_400_BAD_REQUEST,
                          "success": False
                          }
                }
    else:
        return {"message": "successfully updated the specialisation table", "success": True,
                "code": status.HTTP_201_CREATED}


@doctor_specialisation.get("/doctors/specialisations/", tags=["DOCTORS/SPECIALISATIONS"],
                           description="Get specialisations")
async def get_specialisations(active_state: str = Query(None, title="Query parameter for search",
                                                        description="Provide values in type(string)= true/false/getAll")):
    logger.info("###### GET SPECIALISATION ######## ")

    if active_state == "true" or active_state is None:
        return await get_true_specialisation()
    elif active_state == "false":
        return await get_false_specialisation()
    elif active_state == "getAll":
        return await get_all_specialisation()
    else:
        raise CustomExceptionHandler(message="no parameter found", code=status.HTTP_404_NOT_FOUND, success=False,
                                     target="GET-SPECIALISATION")


@doctor_specialisation.get("/doctors/specialisations/{doctor_id}", tags=["DOCTORS/SPECIALISATIONS"],
                           description="Get specialisations")
async def get_specialisations_doctor(doctor_id: int):
    logger.info("###### GET SPECIALISATION FOR SPECIFIC DOCTOR IS CALLED  ########")
    return await get_specialisation_of_doctor(doctor_id=doctor_id)
