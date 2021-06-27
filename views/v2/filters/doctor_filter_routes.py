""" API DESIGN FOR FILTERATION """
from fastapi import APIRouter, Query, Path

app_v2_filters = APIRouter()

""" NEED TO ADD PAGINATION SUPPORT FOR THIS ROUTE """


@app_v2_filters.get("/doctors/explore/", tags=["DOCTORS/FILTERS"],
                    description="Get Specific Specialisation by name")
async def get_specific_specialisation(
        expertise: str = Query(None, title="Query parameter for finding specific "
                                           "specialisation"),
        rating: int = Query(None, title="Query parameter for finding specific "
                                        "specialisation"),
        language: str = Query(None, title="Query parameter for finding specific "
                                          "specialisation")
):
    # make enums of the languages and ratings

    conditions_map = {"expertise": expertise, "rating": rating, "language": language}
    loop_through = {}
    for key, value in conditions_map.items():
        if value is not None:
            loop_through[key] = value