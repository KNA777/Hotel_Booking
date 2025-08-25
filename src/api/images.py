from fastapi import APIRouter, UploadFile

from src.services.images import ImageService

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("", summary="Загрузка изображений")
def upload_images(file: UploadFile):
    ImageService().upload_image(file)
    return {
        "status": "Ok"
    }

