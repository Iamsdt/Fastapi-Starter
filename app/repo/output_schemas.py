from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic.main import BaseModel

# *****************************************************
# Motivation:
# if you required all the output in the same format
# then you can use OutputResponse
# this will output as
"""
{
    data: None,
    message: "Successful",
    response: "OK"
}
"""


# *****************************************************


class SingleMessageSchemas(BaseModel):
    message: str


class ResponseType(str, Enum):
    failed = "FAILED"
    successful = "OK"


T = TypeVar('T')


class OutputResponse(BaseModel, Generic[T]):
    data: T = None
    message: str = ""
    response: ResponseType = ResponseType.successful


# This will return for un auth
def unauth_error_response(message: str):
    return OutputResponse(
        message=message,
        response=ResponseType.failed
    )


# this is for error response
def error_response(message: str):
    return OutputResponse(
        message=message,
        response=ResponseType.failed
    )


# this successful message
def successful_response(data: Any, message: str = ""):
    model = OutputResponse(
        data=data,
        message=message,
    )
    return model


# get hint
def response_hint(model: any):
    return {
        200: OutputResponse[model].dict,
        401: {"detail": "Not authenticated"}
    }
