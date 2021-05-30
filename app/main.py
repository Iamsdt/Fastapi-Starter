import logging

from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend

from app.db import init_db
from app.repo.handle_errors import init_errors_handler
from app.router import init_routes
from app.settings import get_settings
from app.utils.dependencies import init_cors
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


# setup redis
def redis_cache():
    return caches.get(CACHE_KEY)


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend('redis://redis')
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()


@app.get('/')
async def hello(
        cache: RedisCacheBackend = Depends(redis_cache)
):
    in_cache = await cache.get('some_cached_key')
    if not in_cache:
        await cache.set('some_cached_key', 'new_value', 5)

    return {'response': in_cache or 'default'}
