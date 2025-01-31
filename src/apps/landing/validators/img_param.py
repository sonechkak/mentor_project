from django.core.exceptions import ValidationError

from PIL import Image
from django.core.validators import FileExtensionValidator


def validate_image_size(image, size, width, height):
    file_size = image.file.size
    if file_size > size * width * height:
        raise ValidationError(f"Размер файла не должен превышать {size}MB.")

    with Image.open(image) as img:
        if img.width > width or img.height > height:
            raise ValidationError(f"Размер изображения не должен превышать {width}x{height} пикселей.")


def validate_main_image_size(image):
    validate_image_size(image=image, size=3, width=1920, height=1080)


main_image_validators = [
    FileExtensionValidator(allowed_extensions=["jpg", "svg", "png", "webp"]),
    validate_main_image_size,
]

def validate_content_image_size(image):
    validate_image_size(image=image, size=1, width=100, height=4100)

content_image_validators = [
    FileExtensionValidator(allowed_extensions=["jpg", "svg", "png"]),
    validate_content_image_size,
]