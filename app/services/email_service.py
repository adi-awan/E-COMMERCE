from fastapi_mail import FastMail, MessageSchema
from app.core.email import conf
import aiosmtplib
from email.message import EmailMessage

if conf is None:
    return

else:
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587

    EMAIL_USER = "yourgmail@gmail.com"
    EMAIL_PASSWORD = "your_app_password"


    async def send_email(to_email: str, subject: str, html_content: str):

        message = EmailMessage()
        message["From"] = EMAIL_USER
        message["To"] = to_email
        message["Subject"] = subject

        message.set_content(html_content, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=EMAIL_HOST,
            port=EMAIL_PORT,
            start_tls=True,
            username=EMAIL_USER,
            password=EMAIL_PASSWORD,
        )