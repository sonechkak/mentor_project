import pytest

from django.core.exceptions import ValidationError

from src.apps.accounts.validators import NotEmptyValidator


@pytest.fixture
def validator():
    return NotEmptyValidator()


@pytest.mark.parametrize(
    "value, should_raise, expected_error",
    [
        ("непустое значение", False, None),
        ("", True, "Поле не может быть пустым."),
        ("    ", True, "Поле не может быть пустым."),
    ],
)
def test_not_empty_validator(validator, value, should_raise, expected_error):
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
            pytest.fail("ValidationError не должен был быть вызван для непустого значения.")
