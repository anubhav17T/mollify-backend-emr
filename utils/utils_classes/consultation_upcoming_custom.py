from datetime import datetime
from fastapi import status
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from utils.db_functions.db_consultation_function import doctor_custom_day_consultations, fetch_all_form_details
from utils.helper_function.misc import convert_datetime
from utils.logger.logger import logger


class CustomConsultation:
    def __init__(self, field: str,doctor_id:int):
        self.field = field
        self.doctor_id = doctor_id

    @staticmethod
    async def if_field_is_day():
        current_time = datetime.now()
        logger.info("####### CURRENT TIME IS {} #########".format(current_time))
        return convert_datetime(time=current_time),current_time

    async def find_consultation(self):
        if self.field == "day":
            end_time,current_time = await self.if_field_is_day()
            fetch_current_day_open_consultations = await doctor_custom_day_consultations(doctor_id=self.doctor_id,
                                                                                         current_time=current_time,
                                                                                         end_time=end_time)
            return fetch_current_day_open_consultations
        if self.field == "week":
            pass
        if self.field == "month":
            pass

    async def fetch_information(self):
        consultation_information = []
        fetch_field_consultations = await self.find_consultation()
        if not fetch_field_consultations:
            return {"message": "No consultations for today",
                    "success": True,
                    "code": status.HTTP_200_OK,
                    "data": []
                    }
        try:
            for values in fetch_field_consultations:
                items = dict(values)
                if len(items["status"]) == 2:
                    booking_upcoming_information = {"information": [
                        {
                            "status": items["status"][0],
                            "id": items["id"][0],
                            "cancel_reason": items["cancel_reason"][0],
                            "parent_id": items["parent_id"][0]
                        },
                        {
                            "status": items["status"][1],
                            "id": items["id"][1],
                            "cancel_reason": items["cancel_reason"][1],
                            "parent_id": items["parent_id"][1]
                        }
                    ],
                        "patient": {"id": items["patient_id"], "name": items["patient_name"],
                                    "gender": items["gender"], "marital_status": items["marital_status"]},
                        "status": items["status"][1],
                        "id": items["id"][1],
                        "cancel_reason": items["cancel_reason"][1],
                        "parent_id": items["parent_id"][1],
                    }
                else:
                    booking_upcoming_information = {"information": [
                        {
                            "status": items["status"][0],
                            "id": items["id"][0],
                            "cancel_reason": items["cancel_reason"][0],
                            "parent_id": items["parent_id"][0]
                        }
                    ],
                        "patient": {"id": items["patient_id"], "name": items["patient_name"],
                                    "gender": items["gender"], "marital_status": items["marital_status"]},
                        "status": items["status"][0],
                        "id": items["id"][0],
                        "parent_id": items["parent_id"][0],
                    }
                booking_upcoming_information["start_time"] = items["start_time"]
                booking_upcoming_information["end_time"] = items["end_time"]
                booking_upcoming_information["session_type"] = items["session_type"]
                booking_upcoming_information["patient_id"] = items["patient_id"]
                document_info = await fetch_all_form_details(patient_id=items["patient_id"],
                                                             consultation_id=booking_upcoming_information["id"])
                if document_info:
                    temp_array = []
                    for val in document_info:
                        items = dict(val)
                        temp_array.append(
                            {"type": items["document_type"], "url": items["url"], "media_type": items["media_type"]})
                    booking_upcoming_information["document"] = temp_array
                else:
                    booking_upcoming_information["document"] = []
                consultation_information.append(booking_upcoming_information)
        except Exception as Why:
            raise CustomExceptionHandler(message="Something went wrong,cannot able to show upcoming consultations",
                                         code=status.HTTP_404_NOT_FOUND,
                                         success=False,
                                         target="GET-PAST-CONSULTATIONS-DUE_TO {}".format(Why)
                                         )
        else:
            return {"message": "Here is your upcoming consultations",
                    "success": True,
                    "code": status.HTTP_200_OK,
                    "data": consultation_information
                    }



