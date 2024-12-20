import pytest

from django.core.exceptions import ValidationError

from src.apps.accounts.validators import MinimumLengthValidator


@pytest.mark.parametrize(
    "password, should_raise, expected_error",
    [
        ("12345", True, "Пароль должен быть минимум 8 символов"),
        ("1", True, "Пароль должен быть минимум 8 символов"),
        ("", True, "Пароль должен быть минимум 8 символов"),
        ("      ", True, "Пароль должен быть минимум 8 символов"),
        ("12345678", False, None),
        ("abcdefgh123", False, None),
        ("a1b2c3d4", False, None),
        ("very_long_password_123", False, None),
    ],
)
def test_minimum_length_validator(password, should_raise, expected_error):
    """
    Проверяем валидатор для паролей с разной длиной.
    """
    validator = MinimumLengthValidator()

    if should_raise:
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(password)
        assert exc_info.value.messages == [expected_error]
    else:
        try:
            validator.validate(password)
        except ValidationError:
            pytest.fail("ValidationError не должен был быть вызван для корректного пароля.")
