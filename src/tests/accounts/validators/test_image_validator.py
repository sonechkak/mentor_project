from io import BytesIO

import pytest
from PIL import Image

from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile

from src.apps.accounts.validators import ImageValidator


@pytest.fixture
def valid_image():
    """
    Изображение 200x200 пикселей
    """
    img = Image.new("RGB", (200, 200), color="red")
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)
    return ImageFile(img_io, name="valid_image.png")


@pytest.fixture
def oversized_image():
    """
    Изображение 400x400 пикселей
    """
    img = Image.new("RGB", (400, 400), color="red")
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)
    return ImageFile(img_io, name="oversized_image.png")


@pytest.fixture
def large_file_image():
    """
    Изображение 3MB
    """
    img = Image.new("RGB", (100, 100), color="red")
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)

    img_io.seek(0, 2)
    img_io.write(b"\0" * (3 * 1024 * 1024))
    img_io.seek(0)
    return ImageFile(img_io, name="large_file_image.png")


@pytest.fixture
def invalid_format_image():
    """
    Изображение с неверным форматом (GIF).
    """
    img = Image.new("RGB", (200, 200), color="yellow")
    img_io = BytesIO()
    img.save(img_io, format="GIF")
    img_io.seek(0)
    return ImageFile(img_io, name="invalid_format_image.gif")


@pytest.mark.parametrize(
    "image, should_raise, expected_error",
    [
        ("valid_image", False, None),
        ("oversized_image", True, "Размер изображения не должен превышать 300x300 пикселей."),
        ("large_file_image", True, "Размер файла не должен превышать 2MB."),
        ("invalid_format_image", True, "Разрешены только файлы формата jpg и png."),
    ],
)
def test_image_validator(image, should_raise, expected_error, request):
    validator = ImageValidator(file_extension=["jpg", "png"])
    image = request.getfixturevalue(image)

    if should_raise:
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(image)
        assert exc_info.value.message == expected_error
    else:
        try:
            validator.validate(image)
        except ValidationError:
            pytest.fail("ValidationError не должен быть вызван для корректного изображения.")
