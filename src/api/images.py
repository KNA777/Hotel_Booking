import shutil  # для копирования и архивирования файлов

from fastapi import APIRouter, UploadFile

from src.services.images import ImageService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("", summary="Загрузка изображений")
def upload_images(file: UploadFile):
    ImageService().upload_image(file)
