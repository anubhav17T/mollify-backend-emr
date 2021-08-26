import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from utils.logger.logger import logger

html = """\
<html>
  <head></head>
  <body>
    <p>Please Find Reset Password Code Below.<br>
       Hi, Your code is valid for 10 minutes, after 10 minutes please request new one<br>
       <br><br><h3>{code}</h3><br>
    </p>
  </body>
</html>
"""


def send_email(to_email, subject, reset_code):
    message = Mail(
        from_email='support@mollify.in',
        to_emails=to_email,
        subject=subject,
        html_content=html.format(code=reset_code))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        if response.status_code == 200 or 202:
            logger.info("##### EMAIL HAS BEEN SENT TO THE EMAIL {} #########".format(to_email))
            return True
    except Exception as e:
        logger.error("####### UNABLE TO SEND THE EMAIL WITH EXCEPTION {} ###########".format(e))
        return False
