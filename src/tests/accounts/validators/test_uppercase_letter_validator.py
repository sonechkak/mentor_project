import pytest

from django.core.exceptions import ValidationError

from src.apps.accounts.validators import UppercaseLetterValidator


@pytest.fixture
def validator():
    return UppercaseLetterValidator()


@pytest.mark.parametrize(
    "value, should_raise, expected_error",
    [
        ("12345password", True, "Пароль должен содержать хотя бы одну заглавную букву."),
        ("lowercaseletters", True, "Пароль должен содержать хотя бы одну заглавную букву."),
        ("   ", True, "Пароль должен содержать хотя бы одну заглавную букву."),
        ("1234Password", False, None),
        ("S", False, None),
        ("SAKAJHF", False, None),
    ],
)
def test_uppercase_letter_validator(validator, value, should_raise, expected_error):
    """
    Проверяем работу валидатора с разными входными значениями.
    """
    if should_raise:
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(value)
        assert exc_info.value.messages == [expected_error]
    else:
        try:
            validator.validate(value)
        except ValidationError:
            pytest.fail("ValidationError не должен быть вызван для пароля с заглавной буквой.")
