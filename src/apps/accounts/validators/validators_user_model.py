from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

from PIL import Image


name_validators = [
    MinLengthValidator(2, "Поле должно содержать минимум 2 символа."),
    RegexValidator(
        regex="^[a-zA-Zа-яА-ЯёЁ]+$",
        message="Поле может содержать только буквы латиницы и кириллицы.",
    ),
]

email_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    message='Email должен содержать только буквы латиницы, цифры, спец. символы, но без пробелов.'
)

password_validators = [
    MinLengthValidator(8, "Пароль должен содержать минимум 8 символов."),
    RegexValidator(
        regex=r'[A-Z]',
        message="Пароль должен содержать хотя бы одну заглавную букву."
    ),
    RegexValidator(
        regex=r'\d',
        message="Пароль должен содержать хотя бы одну цифру."
    ),
    RegexValidator(
        regex=r'[!@#$%^&*(),.?":{}|<>]',
        message="Пароль должен содержать хотя бы один спец. символ."
    )
]


def validate_image_size(image):
    file_size = image.file.size
    if file_size > 2 * 1024 * 1024:
        raise ValidationError("Размер файла не должен превышать 2MB.")

    # Проверка на максимальный размер изображения (300x300 px)
    img = Image.open(image)
    if img.height > 300 or img.width > 300:
        raise ValidationError("Размер изображения не должен превышать 300x300 пикселей.")
