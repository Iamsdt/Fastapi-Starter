from fastapi import Depends, BackgroundTasks
from fastapi_mail import ConnectionConfig
from fastapi_mail import FastMail, MessageSchema

from app.settings import get_email_config
from app.utils.dependencies import logger


def send_email(email: MessageSchema, config: ConnectionConfig = Depends(get_email_config)) -> bool:
    fm = FastMail(config)
    try:
        # nothing return, so no crash means true
        await fm.send_message(email)
        return True
    except Exception as e:
        logger.exception("Not able to send email", exc_info=e)
        return False


# using background task
def send_email_background(email: MessageSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email)
