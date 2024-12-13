from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator, MaxLengthValidator, FileExtensionValidator

from PIL import Image

title_validators = [
        MinLengthValidator(5, message="Минимум 5 символов"),
        MaxLengthValidator(40, message="Максимум 40 символов")
    ]

slug_validators = [
    MinLengthValidator(1, message="Минимум 1 символ"),
    RegexValidator(
        regex=r'^[a-z0-9-]+$',
        message='Разрешены только строчные буквы (a-z), цифры (0-9) и дефисы (-).'
    ),
]

content_validators = MinLengthValidator(1, message="Минимум 1 символ")

name_validators = [
        MinLengthValidator(1, message="Минимум 1 символ"),
        MaxLengthValidator(30, message="Максимум 30 символов")
    ]


def validate_img_size(max_file_size=None, max_width=None, max_height=None):
    def validate_img(image):
        # Проверяем размер файла
        if max_file_size is not None:
            file_size = image.file.size
            if file_size > max_file_size * 1024 * 1024:
                raise ValidationError(f"Размер файла не должен превышать {max_file_size // (1024 * 1024)} MB.")

        # Проверяем размеры изображения
        try:
            img = Image.open(image)
            width, height = img.size
        except Exception as e:
            raise ValidationError(f"Произошла ошибка при открытии изображения: {e}")
        finally:
            # Закрываем файл
            img.close()

        if max_width is not None and width > max_width:
            raise ValidationError(f"Ширина изображения не должна превышать {max_width} пикселей.")

        if max_height is not None and height > max_height:
            raise ValidationError(f"Высота изображения не должна превышать {max_height} пикселей.")

    return validate_img


article_image_validators = [
    FileExtensionValidator(allowed_extensions=['jpg', 'svg']),
    validate_img_size(max_file_size=3, max_width=1920, max_height=1080)
]

tag_icon_validators = [
    FileExtensionValidator(allowed_extensions=['svg', 'png']),
    validate_img_size(max_file_size=1, max_width=400, max_height=400)
]