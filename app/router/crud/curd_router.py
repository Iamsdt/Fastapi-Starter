import fastapi
from fastapi import Depends
from fastapi_crudrouter import TortoiseCRUDRouter

from app.repo.auth import get_current_user
from app.db.user_details_models import DeviceTable, DeviceTable_Pydantic, LoginHistoryTable, LoginHistoryTable_Pydantic


def add_crud_router(app: fastapi):
    # device table
    router = TortoiseCRUDRouter(
        schema=DeviceTable_Pydantic,
        db_model=DeviceTable,
        prefix="device",
        dependencies=[Depends(get_current_user)],
        create_route=False,
        update_route=False,
    )

    app.include_router(router)

    # author table
    router = TortoiseCRUDRouter(
        schema=LoginHistoryTable_Pydantic,
        db_model=LoginHistoryTable,
        prefix="history",
        dependencies=[Depends(get_current_user)],
        create_route=False,
        update_route=False,
    )

    app.include_router(router)
