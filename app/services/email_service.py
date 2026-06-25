from fastapi_mail import FastMail, MessageSchema
from app.core.email import conf


if conf is None:
    return

else:
    async def send_email(
        email,
        subject,
        body
    ):

        message = MessageSchema(

            subject=subject,

            recipients=[
                email
            ],

            body=body,

            subtype="html"
        )


        fm = FastMail(conf)

        await fm.send_message(
            message
        )