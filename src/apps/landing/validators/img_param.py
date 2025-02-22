import os

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validate_image_size(image, size_mb, width, height):
    # Перемещаем указатель в конец потока, чтобы узнать размер файла
    image.seek(0, os.SEEK_END)
    file_size = image.tell()

    # Преобразуем size_mb из МБ в байты
    max_file_size_in_bytes = size_mb * 1048576

    if file_size > max_file_size_in_bytes:
        raise ValidationError(f"Размер файла не должен превышать {size_mb}MB.")

    # Возвращаемся в начало потока, чтобы корректно открыть изображение
    image.seek(0)

    with Image.open(image) as img:
        if img.width > width or img.height > height:
            raise ValidationError(f"Размер изображения не должен превышать {width}x{height} пикселей.")


def validate_main_image_size(image):
    validate_image_size(image=image, size_mb=3, width=1920, height=1080)


main_image_validators = [
    FileExtensionValidator(allowed_extensions=["jpg", "svg", "png", "webp"]),
    validate_main_image_size,
]

def validate_content_image_size(image):
    validate_image_size(image=image, size_mb=1, width=100, height=4100)

content_image_validators = [
    FileExtensionValidator(allowed_extensions=["jpg", "svg", "png"]),
    validate_content_image_size,
]