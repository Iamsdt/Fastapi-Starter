import os
import shutil
from datetime import datetime
from typing import List, Tuple

from fastapi import UploadFile, Depends

from app.settings import get_settings, Settings


# save single files
def save_file(file: UploadFile, modify_path: str = "", settings: Settings = Depends(get_settings)) -> str:
    x = datetime.now().strftime("%Y%m%d")
    if modify_path:
        path = os.path.join(settings.BASE_URL, settings.MEDIA_URL, modify_path, x)
    else:
        path = os.path.join(settings.BASE_URL, settings.MEDIA_URL, x)

    os.makedirs(path, exist_ok=True)

    with open(path + "/" + file.filename, "wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return path + "/" + file.filename


# save multiples files
def save_files(files: List[UploadFile], modify_path: str = "",
               settings: Settings = Depends(get_settings)) -> Tuple[str, list]:
    li = []
    if modify_path:
        base = os.path.join(settings.BASE_URL, settings.MEDIA_URL, modify_path)
    else:
        base = os.path.join(settings.BASE_URL, settings.MEDIA_URL)

    for file in files:
        path = os.path.join(base, file.filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # save into files
        li.append(path)

    return base, li


# delete file
def delete_file(path: str):
    os.remove(path)
