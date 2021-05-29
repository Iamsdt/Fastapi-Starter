from pydantic.main import BaseModel


class VerifyAccount(BaseModel):
    user_id: str
    otp: int
    client_secret: str


class TokenSchemas(BaseModel):
    access_token: str
    token_type: str
