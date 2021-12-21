from datetime import datetime
import calendar
from pytz import timezone


async def check_password_length(new):
    if len(new) <= 6:
        return False
    return True


def convert_datetime(time):
    now = datetime.now(timezone("Asia/Kolkata"))
    current_time = str(now.strftime("%d/%m/%Y"))
    current_time = current_time + " 23:59:51"
    current_time_object = datetime.strptime(current_time, "%d/%m/%Y %H:%M:%S")
    return current_time_object


def get_last_date(year, month):
    date = calendar.monthrange(year, month)
    return date[1]


def check_for_cancellation_time(cancel_time):
    dt = datetime.now(timezone("Asia/Kolkata"))
    if cancel_time.date() == dt.date():
        return False
    return True


def list_to_set_with_case_conversion(val: list, ops):

    if val:
        if len(val) <= 1:
            val.append('help')
        if ops == 1:
            val = tuple(set(map(lambda lang: lang.lower(), val)))
        elif ops == 2:
            val = tuple(set(map(lambda lang: lang.upper(), val)))
        return val
    else:
        return None

# c = "30/9/2021 23:59:51"
# current_time_object = datetime.strptime(c, "%d/%m/%Y %H:%M:%S")
# print(current_time_object)
