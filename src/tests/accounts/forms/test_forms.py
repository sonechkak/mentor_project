import pytest

from src.apps.accounts.forms import RegisterForm


@pytest.mark.django_db
def test_clean_email_valid(valid_data_form_register):
    """Тест корректной валидации email."""
    form = RegisterForm(data=valid_data_form_register)
    assert form.is_valid()
    assert form.cleaned_data["email"] == valid_data_form_register["email"]


@pytest.mark.django_db
def test_clean_email_duplicate(valid_data_form_register, user_model):
    """Тест, что форма вызывает ошибку для существующего email."""
    user_model.objects.create_user(
        first_name="John", email=valid_data_form_register["email"], password="Userpassword123/*-"
    )
    form = RegisterForm(data=valid_data_form_register)
    assert not form.is_valid()
    assert "email" in form.errors
    assert form.errors["email"] == ["Пользователь с таким email уже существует."]


@pytest.mark.django_db
def test_clean_password2_mismatch(valid_data_form_register):
    """Тест, что пароли должны совпадать."""
    valid_data_form_register["password2"] = "DifferentPass123/*-"
    form = RegisterForm(data=valid_data_form_register)
    assert not form.is_valid()
    assert "password2" in form.errors
    assert form.errors["password2"] == ["Пароли не совпадают!"]


@pytest.mark.django_db
def test_save_create_user(valid_data_form_register, user_model):
    """Тест, что метод save создаёт пользователя."""
    form = RegisterForm(data=valid_data_form_register)
    assert form.is_valid()  # Убедиться, что данные валидны
    user = form.save()
    assert user_model.objects.filter(email=valid_data_form_register["email"]).exists()
    assert user.first_name == valid_data_form_register["first_name"]


@pytest.mark.django_db
def test_save_without_commit(valid_data_form_register, user_model):
    """Тест сохранения пользователя без сохранения в БД."""
    form = RegisterForm(data=valid_data_form_register)
    assert form.is_valid()
    user = form.save(commit=False)
    assert not user_model.objects.filter(email=valid_data_form_register["email"]).exists()
    assert user.email == valid_data_form_register["email"]
