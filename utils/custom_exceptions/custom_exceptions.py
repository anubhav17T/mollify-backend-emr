""" CLASS FOR RAISING CUSTOM EXCEPTIONS """


class Error(Exception):
    """Base class for other exceptions"""
    pass


""" CUSTOM EXCEPTIONS """


class HashPasswordError(Error):
    """ RAISED WHEN HASH FUNCTION UNABLE TO HASH A STRING OR PASSWORD """
    pass


class CustomException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class CustomExceptionHandler(Exception):
    def __init__(self, message: str, target: str, success: bool, code: int):
        self.message = message
        self.target = target
        self.success = success
        self.code = code


class BadRequestCustomException(Exception):
    def __init__(self, name: str):
        self.name = name


class ConflictCustomException(Exception):
    def __init__(self, name: str):
        self.name = name
