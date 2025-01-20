import shutil  #для копирования и архивирования файлов

from fastapi import APIRouter, UploadFile
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("", summary="Загрузка изображений")
def upload_images(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(fsrc=file.file, fdst=new_file)

        resize_image.delay(image_path)

    return {"status": "Задача в обработке"}
