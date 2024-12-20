import re
from string import punctuation
from typing import Optional, TYPE_CHECKING

from django.core.exceptions import ValidationError

from PIL import Image

if TYPE_CHECKING:
    from src.apps.accounts.models import User
    from django.core.files.images import ImageFile


class NotEmptyValidator:
    """
    Валидатор для проверки, что поле не пустое.
    """

    def validate(self, value: str, user: Optional["User"] = None) -> None:
        if not value or value.strip() == "":
            raise ValidationError("Поле не может быть пустым.")


class MinimumLengthValidator:
    """
    Валидатор для проверки минимальной длины:
    - Минимум 8 символов
    """

    MIN_LENGTH = 8

    def validate(self, password: str, user: Optional["User"] = None) -> None:
        if len(password) < self.MIN_LENGTH:
            raise ValidationError(f"Пароль должен быть минимум {self.MIN_LENGTH} символов")


class SpecialSymbolValidator:
    """
    Валидатор для проверки наличия хотя бы одного спецсимвола в пароле.
    """

    SPECIAL_SYMBOLS_PATTERN = re.compile(f"[{re.escape(punctuation)}]")

    def validate(self, password: str, user: Optional["User"] = None) -> None:
        if not self.SPECIAL_SYMBOLS_PATTERN.search(password):
            raise ValidationError("Пароль должен содержать хотя бы один спец. символ.")


class UppercaseLetterValidator:
    """
    Валидатор для проверки наличия хотя бы одной заглавной буквы в пароле.
    """

    UPPERCASE_LETTERS_PATTERN = re.compile(r"[A-Z]")

    def validate(self, password: str, user: Optional["User"] = None) -> None:
        if not self.UPPERCASE_LETTERS_PATTERN.search(password):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")


class NumericCharacterValidator:
    """
    Валидатор для проверки наличия хотя бы одной цифры в пароле.
    """

    DIGITS_PATTERN = re.compile(r"[0-9]")

    def validate(self, password: str, user: Optional["User"] = None) -> None:
        if not self.DIGITS_PATTERN.search(password):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")


class NameValidator:
    """
    Валидатор для проверки имени:
    - Минимум 2 символа
    - Максимум 30 символов
    - Только буквы латиницы и кириллицы
    """

    MIN_LENGTH = 2
    MAX_LENGTH = 30
    LETTERS_PATTERN = re.compile(r"^[a-zA-Zа-яА-ЯёЁ]{2,30}$")

    def validate(self, value: str, user: Optional["User"] = None) -> None:
        if len(value) < self.MIN_LENGTH:
            raise ValidationError("Поле должно содержать минимум 2 символа.")

        if len(value) > self.MAX_LENGTH:
            raise ValidationError("Поле должно содержать максимум 30 символов.")

        if not self.LETTERS_PATTERN.match(value):
            raise ValidationError("Поле может содержать только буквы латиницы и кириллицы.")


class EmailValidator:
    """
    Валидатор для проверки корректного email:
    - Максимум 100 символов
    - Допускаются буквы латиницы, цифры, спец. символы
    - Не допускаются пробелы
    """

    MAX_LENGTH = 100
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    def validate(self, value: str, user: Optional["User"] = None) -> None:
        if len(value) > self.MAX_LENGTH:
            raise ValidationError("Email не должен превышать 100 символов.")

        if " " in value:
            raise ValidationError("Email не должен содержать пробелы.")

        if not self.EMAIL_PATTERN.match(value):
            raise ValidationError(
                "Email должен содержать только буквы латиницы, цифры, спец. символы, "
                "но без пробелов."
            )


class ImageValidator:
    """
    Валидатор для проверки image:
    - Размер файла < 2MB
    - Размер изображения <= 300x300 пикселей
    - Форматы файла: jpg, png
    """

    def validate(self, image: "ImageFile", user: Optional["User"] = None) -> None:
        file_size = image.size
        if file_size > 2 * 1024 * 1024:
            raise ValidationError("Размер файла не должен превышать 2MB.")

        if image.name.split(".")[-1].lower() not in ["jpg", "png"]:
            raise ValidationError("Разрешены только файлы формата jpg и png.")

        with Image.open(image.file) as img:
            if img.width > 300 or img.height > 300:
                raise ValidationError("Размер изображения не должен превышать 300x300 пикселей.")
