import os.path
from time import sleep

from PIL import Image

from src.tasks.celery_app import celery_instance


@celery_instance.task
def test_task():
    sleep(5)
    print("!!!!!!!!")


@celery_instance.task
def resize_image(image_path: str):
    sizes = [i for i in range(400, 1800, 10)]
    output_folder = "src/static/images"  # путь к папке куда сохранять изображение

    img = Image.open(image_path)  # открываем изображение

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)  # получаем имя и расширение картинки

    for size in sizes:
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        # имя нового файла
        new_file_name = f"{name}_{size}px{ext}"

        # полный путь для сохранения
        output_path = os.path.join(output_folder, new_file_name)

        # сохраняем изображение
        img_resized.save(output_path)

    print(f"Изображение сохранено в слудующих размерах : {sizes} в папке {output_folder}")
