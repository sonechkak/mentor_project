import os

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    FileExtensionValidator,
)

min_one_symbol_validator = MinLengthValidator(1, message="Минимум 1 символ")

min_five_symbols_validator = MinLengthValidator(5, message="Минимум 5 символов")

slug_validators = [
    MinLengthValidator(1, message="Минимум 1 символ"),
    RegexValidator(
        regex=r"^[a-z0-9-_]+$",
        message="Разрешены только строчные буквы (a-z), цифры (0-9) и дефисы (-).",
    ),
]

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


def validate_article_image_size(image):
    validate_image_size(image=image, size_mb=3, width=1920, height=1080)


article_image_validators = [
    FileExtensionValidator(allowed_extensions=["jpg", "svg"]),
    validate_article_image_size,
]

def validate_tag_icon_size(image):
    validate_image_size(image=image, size_mb=1, width=400, height=400)


tag_icon_validators = [
    FileExtensionValidator(allowed_extensions=["svg", "png"]),
    validate_tag_icon_size,
]

hex_color_validator = RegexValidator(
    regex=r'^(?!#ffffff|#FFFFFF)(#(?:[0-9a-fA-F]{3}){1,2})$',
    message="Введите цвет в HEX-формате, кроме белого (#FFFFFF). Близкие к белому оттенки не рекомендуются."
)