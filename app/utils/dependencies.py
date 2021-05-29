import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.settings import get_settings

logger = logging.getLogger("fastapi")


def verify_client(client_id: str, client_secret) -> bool:
    return get_settings().APP_CLIENT_ID == client_id and client_secret == get_settings().APP_CLIENT_SECRET


def init_cors(app: FastAPI):
    # now setup cors
    origins = [
        "http://localhost",
        "http://localhost:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
