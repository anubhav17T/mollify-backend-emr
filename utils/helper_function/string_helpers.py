from typing import List
from constants.const import ADDING_YEARS

QUERY_FOR_TIME_SLOT_DAYS = "day="
QUERY_FOR_TIME_SLOT_DAYS_HELPER = " OR day="
from models.time_slot_configuration import Status


def string_to_lower(string_value: str) -> str:
    return string_value.lower()


def string_concatenation_with_years(string_value: str) -> str:
    return string_value + ADDING_YEARS


def check_length(string: str):
    if len(string) >= 500 or len(string) <= 40:
        return False
    return True


def make_days_query_from_string(days: str, query: str, query_helper: str):
    """:DAYS ARE THE QUERY PARAMETER FOR SELECTED DAYS TO SEARCH DOCTOR
       :QUERY IS THE DATABASE QUERY
    """
    days = days.split(",")
    try:
        for valid_enums in days:
            Status(valid_enums)
    except Exception:
        raise Exception("DAYS IS NOT VALID ENUM, PLEASE CHECK THE QUERY AGAIN")
    for char in range(0, len(days)):
        query += "'{}'".format(days[char]) + query_helper
    string = query.rstrip(query_helper)

    return string
