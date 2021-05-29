from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.settings import get_settings


def get_db_uri(user, passwd, host, db, port):
    return f"postgres://{user}:{passwd}@{host}:{port}/{db}"


TORTOISE_ORM = {
    "connections": {
        "default": get_db_uri(
            user=get_settings().POSTGRESQL_USERNAME,
            passwd=get_settings().POSTGRESQL_PASSWORD,
            host=get_settings().POSTGRESQL_HOSTNAME,
            port=get_settings().POSTGRESQL_PORT,
            db=get_settings().POSTGRESQL_DATABASE,
        )
    },  # postgresql
    # "connections": {"default": "mysql://root:123456@127.0.0.1:3306/test"}, # mysql connections
    # "connections": {"default": "sqlite://:memory:"}, # sqlite in memory database
    # "connections": {"default": "sqlite://./podcast.db"},
    "apps": {
        "models": {
            "models": [
                "app.db.user_model",
                "app.db.user_details_models",
                "aerich.models"  # For handling migrations
            ],
            "default_connection": "default",
        },
    },
}


# Init database
def init_db(app: FastAPI):
    # for testing lets use, sql
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
