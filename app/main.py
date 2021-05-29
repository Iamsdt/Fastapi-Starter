import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.db import init_db
from app.utils.dependencies import init_cors
from app.repo.handle_errors import init_errors_handler
from app.router import init_routes
from app.settings import get_settings
from app.utils.logs import init_logger

app = FastAPI(
    title=get_settings().APP_NAME,
    version=get_settings().APP_VERSION,
    debug=get_settings().debug,
    docs_url="/",
    swagger_ui_oauth2_redirect_url="/auth/token",
    default_response_class=ORJSONResponse,
)

# init logging
init_logger(logging.DEBUG)

# init database
init_db(app)

# init cors
init_cors(app)

# init error handler
init_errors_handler(app)

# init routes
init_routes(app)
