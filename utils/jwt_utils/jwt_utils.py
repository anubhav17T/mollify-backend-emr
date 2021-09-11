import jwt
from jwt import PyJWTError
from pydantic import ValidationError
from datetime import datetime, timedelta
from constants.const import JWT_EXPIRATION_TIME, JWT_SECRET_KEY, JWT_ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from utils.db_functions.db_functions import find_exist_user, find_exist_username_email
from models.doctor import Doctor
from utils.db_functions.db_functions import find_black_list_token
from utils.custom_exceptions.custom_exceptions import CustomExceptionHandler


async def create_access_token(data: dict, expire_delta: timedelta = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/doctors/login"
)


def get_token_user(token: str = Depends(oauth2_scheme)):
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        print(username)
        if username is None:
            raise credential_exception
        # Check blacklist token
        black_list_token = await find_black_list_token(token)
        if black_list_token:
            print("error in creds")
            raise credential_exception
        # Check if user exist or not
        result = await find_exist_username_email(check=username)
        if not result:
            raise CustomExceptionHandler(message="You are not registered yet,please register yourself",
                                         code=status.HTTP_404_NOT_FOUND,
                                         success=False,
                                         target="JWT-VERIFICATION"
                                         )
        return {"id":result["id"],
                "username":result["username"],
                "full_name":result["full_name"],
                "mail":result["mail"],
                "phone_number":result["phone_number"],
                "gender":result["gender"],
                "experience":result["experience"],
                "url":result["url"],
                "about":result["about"]
                }
    except (PyJWTError, ValidationError):
        raise credential_exception
