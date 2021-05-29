from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.utils.dependencies import logger
from app.repo.output_schemas import error_response


def init_errors_handler(app: FastAPI):
    # handle exception
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: Exception):
        logger.error("HTTP exception" + str(request.base_url), exc_info=exc)
        return JSONResponse(error_response(str(exc)).dict(), status_code=401)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: Exception):
        logger.error("Value error exception" + str(request.base_url), exc_info=exc)
        return JSONResponse(error_response(str(exc)).dict(), status_code=422)

    @app.exception_handler(DoesNotExist)
    async def not_found_exception_handler(request: Request, exc: Exception):
        logger.error("Not found exception" + str(request.base_url), exc_info=exc)
        return JSONResponse(error_response(str(exc)).dict(), status_code=404)

    @app.exception_handler(IntegrityError)
    async def not_found_exception_handler(request: Request, exc: Exception):
        logger.error("Integrity exception" + str(request.base_url), exc_info=exc)
        return JSONResponse(error_response(str(exc)).dict(), status_code=404)
