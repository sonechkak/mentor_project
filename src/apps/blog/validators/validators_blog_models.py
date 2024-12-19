from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator, FileExtensionValidator

from PIL import Image


min_one_symbol_validator = MinLengthValidator(1, message="Минимум 1 символ")

min_five_symbols_validator = MinLengthValidator(5, message="Минимум 5 символов")

slug_validators = [
    MinLengthValidator(1, message="Минимум 1 символ"),
    RegexValidator(
        regex=r'^[a-z0-9-]+$',
        message='Разрешены только строчные буквы (a-z), цифры (0-9) и дефисы (-).'
    ),
]
def validate_article_image_size(image):
    file_size = image.file.size
    if file_size > 3 * 1024 * 1024:
        raise ValidationError("Размер файла не должен превышать 2MB.")

    # Проверка на максимальный размер изображения (1920x1080 px)
    with Image.open(image) as img:
        if  img.width > 1920 or img.height > 1080:
            raise ValidationError("Размер изображения не должен превышать 1920x1080 пикселей.")


article_image_validators = [
    FileExtensionValidator(allowed_extensions=['jpg', 'svg']),
    validate_article_image_size,
]

def validate_tag_icon_size(image):
    file_size = image.file.size
    if file_size > 1 * 1024 * 1024:
        raise ValidationError("Размер файла не должен превышать 2MB.")

    # Проверка на максимальный размер изображения (400x400 px)
    with Image.open(image) as img:
        if  img.width > 400 or img.height > 400:
            raise ValidationError("Размер изображения не должен превышать 400x400 пикселей.")

tag_icon_validators = [
    FileExtensionValidator(allowed_extensions=['svg', 'png']),
    validate_tag_icon_size,
]
