from typing import List

from app.settings import get_email_config
from app.utils.dependencies import logger
from fastapi import BackgroundTasks, Depends
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema


async def send_email(email: MessageSchema, config: ConnectionConfig = Depends(get_email_config)) -> bool:
    fm = FastMail(config)
    try:
        # nothing return, so no crash means true
        await fm.send_message(email)
        return True
    except Exception as e:
        logger.exception("Not able to send email", exc_info=e)
        return False


async def send_email_bulk(emails: List[MessageSchema], config: ConnectionConfig = Depends(get_email_config)) -> List[MessageSchema]:
    fm = FastMail(config)

    failed = []

    for email in emails:
        try:
            # nothing return, so no crash means true
            await fm.send_message(email)
        except Exception as e:
            failed.append(email)
            logger.exception("Not able to send email", exc_info=e)

    return failed


# using background task
def send_email_background(email: MessageSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email)


# using background task
def send_email_bulk_background(emails: List[MessageSchema], background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_bulk, emails)
