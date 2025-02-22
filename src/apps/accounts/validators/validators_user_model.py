import re
from string import punctuation
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from PIL import Image

if TYPE_CHECKING:
    from django.core.files.images import ImageFile


@deconstructible
class NotEmptyValidator:
    """
    Валидатор для проверки, что поле не пустое.
    """

    def __call__(self, value: str):
        self.validate(value)

    def validate(self, value: str) -> None:
        if not value or value.strip() == "":
            raise ValidationError("Поле не может быть пустым.")


@deconstructible
class MinMaxLengthPasswordValidator:
    """
    Валидатор для проверки длины пароля:
    - Минимум 8 символов
    - Максимум 128 символов
    """

    def __init__(self, min_length: int = 8, max_length: int = 128) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, password: str):
        self.validate(password)

    def validate(self, password: str) -> None:
        if len(password) < self.min_length:
            raise ValidationError(f"Пароль должен быть минимум {self.min_length} символов")

        if len(password) > self.max_length:
            raise ValidationError(f"Пароль должен быть максимум {self.max_length} символов")


@deconstructible
class SpecialSymbolValidator:
    """
    Валидатор для проверки наличия хотя бы одного спецсимвола в пароле.
    """

    SPECIAL_SYMBOLS_PATTERN = re.compile(f"[{re.escape(punctuation)}]")

    def __call__(self, password: str):
        self.validate(password)

    def validate(self, password: str) -> None:
        if not self.SPECIAL_SYMBOLS_PATTERN.search(password):
            raise ValidationError("Пароль должен содержать хотя бы один спец. символ.")


@deconstructible
class UppercaseLetterValidator:
    """
    Валидатор для проверки наличия хотя бы одной заглавной буквы в пароле.
    """

    UPPERCASE_LETTERS_PATTERN = re.compile(r"[A-Z]")

    def __call__(self, password: str):
        self.validate(password)

    def validate(self, password: str) -> None:
        if not self.UPPERCASE_LETTERS_PATTERN.search(password):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")


@deconstructible
class NumericCharacterValidator:
    """
    Валидатор для проверки наличия хотя бы одной цифры в пароле.
    """

    DIGITS_PATTERN = re.compile(r"[0-9]")

    def __call__(self, password: str):
        self.validate(password)

    def validate(self, password: str) -> None:
        if not self.DIGITS_PATTERN.search(password):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")


@deconstructible
class NameValidator:
    """
    Валидатор для проверки имени:
    - Минимум 2 символа
    - Максимум 30 символов
    - Только буквы латиницы и кириллицы
    """

    LETTERS_PATTERN = re.compile(r"^[a-zA-Zа-яА-ЯёЁ]{2,30}$")

    def __init__(self, min_length: int = 2, max_length: int = 30) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, value: str):
        self.validate(value)

    def validate(self, value: str) -> None:
        if len(value) < self.min_length:
            raise ValidationError(f"Поле должно содержать минимум {self.min_length} символа.")

        if len(value) > self.max_length:
            raise ValidationError(f"Поле должно содержать максимум {self.max_length} символов.")

        if not self.LETTERS_PATTERN.match(value):
            raise ValidationError("Поле может содержать только буквы латиницы и кириллицы.")


@deconstructible
class EmailValidator:
    """
    Валидатор для проверки корректного email:
    - Максимум 100 символов
    - Допускаются буквы латиницы, цифры, спец. символы
    - Не допускаются пробелы
    """

    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    def __init__(self, max_length: int = 100):
        self.max_length = max_length

    def __call__(self, value: str):
        self.validate(value)

    def validate(self, value: str) -> None:
        if len(value) > self.max_length:
            raise ValidationError("Email не должен превышать 100 символов.")

        if " " in value:
            raise ValidationError("Email не должен содержать пробелы.")

        if not self.EMAIL_PATTERN.match(value):
            raise ValidationError(
                "Email должен содержать только буквы латиницы, цифры, спец. символы, "
                "но без пробелов."
            )


@deconstructible
class ImageValidator:
    """
    Валидатор для проверки image:
    - Размер файла < 2MB
    - Размер изображения <= 300x300 пикселей
    - Форматы файла: jpg, png  ["jpg", "png"]
    """

    def __init__(self, file_extension: list[str]):
        self.file_extension = file_extension

    def __call__(self, image: "ImageFile"):
        self.validate(image)

    def validate(self, image: "ImageFile") -> None:
        file_size = image.size
        if file_size > 2 * 1024 * 1024:
            raise ValidationError("Размер файла не должен превышать 2MB.")

        if image.name.split(".")[-1].lower() not in self.file_extension:
            raise ValidationError("Разрешены только файлы формата jpg и png.")

        with Image.open(image.file) as img:
            if img.width > 300 or img.height > 300:
                raise ValidationError("Размер изображения не должен превышать 300x300 пикселей.")
