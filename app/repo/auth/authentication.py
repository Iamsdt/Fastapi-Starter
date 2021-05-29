from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.db.user_model import UserTable
from app.settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password, user: UserTable) -> bool:
    return pwd_context.verify(plain_password, user.hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def generate_token(username) -> str:
    # generate based on username
    data = {"username": username}
    # don't care about token expire
    # we will update on every login
    encoded_jwt = jwt.encode(data, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    user = await UserTable.filter(token=token).exists()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # return await UserTable.filter(token=token).first()
    return token
