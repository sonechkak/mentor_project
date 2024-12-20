import pytest

from django.core.exceptions import ValidationError

from src.apps.accounts.validators import EmailValidator


@pytest.fixture
def validator():
    return EmailValidator()


@pytest.mark.parametrize(
    "value, should_raise, expected_error",
    [
        # Невалидные значения
        ("   ", True, "Email не должен содержать пробелы."),
        ("a" * 101 + "@example.com", True, "Email не должен превышать 100 символов."),
        ("invalid email@example.com", True, "Email не должен содержать пробелы."),
        (
            "invalid@exam_ple.com",
            True,
            "Email должен содержать только буквы латиницы, цифры, спец. символы, но без пробелов.",
        ),
        (
            "invalid@.com",
            True,
            "Email должен содержать только буквы латиницы, цифры, спец. символы, но без пробелов.",
        ),
        (
            "@example.com",
            True,
            "Email должен содержать только буквы латиницы, цифры, спец. символы, но без пробелов.",
        ),
        (
            "invalid@com",
            True,
            "Email должен содержать только буквы латиницы, цифры, спец. символы, но без пробелов.",
        ),
        # Валидные значения
        ("valid.email@example.com", False, None),
        ("valid_email123@example.com", False, None),
        ("user123+test@example-domain.com", False, None),
    ],
)
def test_email_validator(validator, value, should_raise, expected_error):
    """
    Проверяем работу валидатора для email с разными входными значениями.
    """
    if should_raise:
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(value)
        assert exc_info.value.messages == [expected_error]
    else:
        try:
            validator.validate(value)
        except ValidationError:
            pytest.fail("ValidationError не должен быть вызван для валидного email.")
