import pytest
from PIL import Image
from io import BytesIO
from django.core.exceptions import ValidationError
from celery.contrib.testing.worker import start_worker

from .validators import validate_article_image_size


@pytest.fixture(scope="module")
def worker():
    with start_worker() as w:
        yield w


@pytest.fixture
def create_test_image(width, height):
    """Создает изображение заданных размеров"""
    file = BytesIO()
    image = Image.new('RGB', (width, height))
    image.save(file, 'jpeg')
    file.name = 'test.jpg'
    file.seek(0)
    return file


def test_validate_article_image_size_correct_filesize(create_test_image):
    """Проверяет, что изображение с правильным размером проходит валидацию."""
    image = create_test_image(800, 600)
    try:
        validate_article_image_size(image)
    except ValidationError as e:
        pytest.fail(f"Валидация прошла неудачно: {e}")


def test_validate_article_image_size_large_filesize(create_test_image):
    """Проверяет, что изображение с неправильным размером файла вызывает ошибку."""
    image = create_test_image(5000, 5000)
    image.file.size = 4 * 1024 * 1024  # 4 MB
    with pytest.raises(ValidationError) as excinfo:
        validate_article_image_size(image)
    assert str(excinfo.value) == "Размер файла не должен превышать 2MB."


def test_validate_article_image_size_large_resolution(create_test_image):
    """Проверяет, что изображение с неправильным разрешением вызывает ошибку."""
    image = create_test_image(2048, 1152)
    with pytest.raises(ValidationError) as excinfo:
        validate_article_image_size(image)
    assert str(excinfo.value) == "Размер изображения не должен превышать 1920x1080 пикселей."


def test_validate_article_image_size_small_resolution(create_test_image):
    """Проверяет, что изображение с маленьким разрешением проходит валидацию."""
    image = create_test_image(640, 480)
    try:
        validate_article_image_size(image)
    except ValidationError as e:
        pytest.fail(f"Валидация прошла неудачно: {e}")