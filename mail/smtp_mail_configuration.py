import smtplib, ssl
from email.mime.multipart import MIMEMultipart


def send_email(receiver_email,subject,sender_email="noreply.mollify@gmail.com",password="Wemollify@12345"):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = "noreply.mollify@gmail.com"
    message["To"] = receiver_email

    message = """
    This is an e-mail message to be sent in HTML format
    """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message
        )


