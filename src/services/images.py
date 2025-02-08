import shutil
from src.tasks.tasks import resize_image
from fastapi import UploadFile

from src.services.base import BaseService


class ImageService(BaseService):
    def upload_image(self, file: UploadFile):

        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(fsrc=file.file, fdst=new_file)

            resize_image.delay(image_path)

        return {"status": "Задача в обработке"}