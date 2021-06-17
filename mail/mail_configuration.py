from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List


html = """
<p>Reset Password Information</p> 
"""

conf = ConnectionConfig(
    MAIL_USERNAME="noreply.mollify@gmail.com",
    MAIL_PASSWORD="Wemollify@12345",
    MAIL_FROM="noreply.mollify@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


async def send_mail(subject: str, recipient: List, message: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipient,
        body=message,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})