""" API DESIGN FOR FILTRATION """
from fastapi import APIRouter, Query, Path

app_v2_filters = APIRouter()


# todo: Need to add rating support and pagination for this route

@app_v2_filters.get("/doctors/explore/", tags=["DOCTORS/FILTERS"],
                    description="Get Specific Specialisation by name")
async def get_specific_specialisation(expertise: str = Query(None, title="Query parameter for finding specific "
                                                                         "specialisation"),
                                      language: str = Query(None, title="Query parameter for finding specific "
                                                                        "specialisation")):
    if expertise is None and language is None:
        pass


    else:
        pass
