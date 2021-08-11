from app.db.user_model import UserTable, UserTable_Pydantic
from app.repo.auth import generate_token, get_current_user, get_password_hash
from app.repo.output_schemas import (OutputResponse, SingleMessageSchemas,
                                     successful_response)
from app.repo.schemas.user_schemas import TokenSchemas, VerifyAccount
from app.router.auth.auth_helper import (check_client, check_login,
                                         update_user_token)
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)


@router.post("/login", response_model=OutputResponse[UserTable_Pydantic])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # check client is correct or not
    check_client(form_data)

    user = await UserTable.get(email=form_data.username)
    # check user is ready to login or not
    check_login(form_data, user)

    # when use logged in we will regenerate token
    # this will prevent using same account
    user1 = await update_user_token(user)

    res = await UserTable_Pydantic.from_tortoise_orm(user1)
    return successful_response(res, "")


@router.post("/signup", response_model=OutputResponse[UserTable_Pydantic])
async def signup(form_data: OAuth2PasswordRequestForm = Depends(), fullname=Form(...)):
    # check client is correct or not
    check_client(form_data)

    password = get_password_hash(form_data.password)
    token = generate_token(form_data.username)

    user = await UserTable.create(
        email=form_data.username,
        fullname=fullname,
        hashed_password=password,
        token=token
    )

    res = await UserTable_Pydantic.from_tortoise_orm(user)

    return successful_response(res, "")


@router.post("/reset", response_model=OutputResponse[SingleMessageSchemas])
async def forget_password(email=Form(...)):
    return {"access_token": "token", "token_type": "bearer"}


@router.post("/reset/password", response_model=OutputResponse[UserTable_Pydantic])
async def update_password(user_id=Form(...), otp=Form(...), password=Form(...)):
    return {"access_token": "token", "token_type": "bearer"}


@router.post("/request/otp", response_model=OutputResponse[SingleMessageSchemas])
async def request_account(email=Form(...)):
    return {"access_token": "token", "token_type": "bearer"}


@router.post("/verify", response_model=UserTable_Pydantic)
async def verify_account(verify: VerifyAccount):
    return {"access_token": "token", "token_type": "bearer"}


@router.post("/token/refresh", response_model=OutputResponse[TokenSchemas])
async def refresh_jwt(user: str = Depends(get_current_user)):
    user = await UserTable.get(token=user)
    user = await update_user_token(user)
    return {"access_token": user.token, "token_type": "bearer"}


# this function is used for swagger ui login
@router.post("/token", response_model=TokenSchemas)
async def obtain_token(form_data: OAuth2PasswordRequestForm = Depends()):
    check_client(form_data)
    user = await UserTable.get(email=form_data.username)
    return {"access_token": user.token, "token_type": "bearer"}
