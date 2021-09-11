async def check_password_length(new):
    if len(new) <=6:
        return False
    return True
