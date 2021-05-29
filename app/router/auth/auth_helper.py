from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.repo.auth import generate_token, verify_password
from app.db.user_model import UserTable
from app.utils.dependencies import verify_client
from app.repo.output_schemas import error_response


def check_client(form_data: OAuth2PasswordRequestForm):
    res = verify_client(form_data.client_id, form_data.client_secret)
    # if res is false, then this is not coming from somewhere else
    if not res:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid application credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def update_user_token(user: UserTable) -> UserTable:
    token = generate_token(user.email)
    res = await user.update_from_dict({"token": token})
    return res


def check_login(form_data: OAuth2PasswordRequestForm, user: UserTable):
    pass_status = verify_password(form_data.password, user)

    if not pass_status:
        return error_response("Wrong password!")

    if not user.is_active:
        return error_response("Your account is disabled")

    if not user.is_verified:
        return error_response("Your account is not verified, please verify your account")
