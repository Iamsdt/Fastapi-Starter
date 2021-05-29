from fastapi import FastAPI

from app.router.auth import auth
from .crud.curd_router import add_crud_router


def init_routes(app: FastAPI):
    app.include_router(auth.router)
    # crud router
    add_crud_router(app)
