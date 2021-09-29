from datetime import datetime
import calendar


async def check_password_length(new):
    if len(new) <= 6:
        return False
    return True


def convert_datetime(time):
    now = datetime.now()
    current_time = str(now.strftime("%d/%m/%Y"))
    current_time = current_time + " 23:59:51"
    current_time_object = datetime.strptime(current_time, "%d/%m/%Y %H:%M:%S")
    return current_time_object


def get_last_date(year,month):
    date = calendar.monthrange(year, month)
    return date[1]


c = "30/9/2021 23:59:51"
current_time_object = datetime.strptime(c, "%d/%m/%Y %H:%M:%S")
print(current_time_object)