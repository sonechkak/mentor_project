import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from rest_framework.test import APIClient


@pytest.fixture
def user_model():
    """Фикстура возвращает модель User."""
    return get_user_model()


@pytest.fixture
def register_url():
    """Фикстура возвращает url регистрации"""
    return reverse("accounts:register")


@pytest.fixture
def login_url():
    """Фикстура возвращает url логина"""
    return reverse("accounts:login")


@pytest.fixture
def home_url():
    """Фикстура возвращает home url (главная страница)"""
    return reverse("accounts:home")


@pytest.fixture
def valid_data_form_register():
    """Корректные данные для формы регистрации."""
    return {
        "first_name": "John",
        "email": "john@example.com",
        "password1": "Userpassword123/*-",
        "password2": "Userpassword123/*-",
    }


@pytest.fixture
def user_data():
    return {
        "first_name": "User",
        "email": "user@example.com",
        "password": "Userpassword123/*-",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False,
        "is_admin": False,
    }


@pytest.fixture
def superuser_data():
    return {
        "first_name": "Admin User",
        "email": "admin@example.com",
        "password": "Adminpassword123/*-",
        "is_active": True,
        "is_admin": True,
        "is_staff": True,
        "is_superuser": True,
    }


@pytest.fixture
def user_data_valid_for_serializer():
    return {
        "first_name": "User",
        "email": "user@example.com",
        "password": "Userpassword123/*-",
    }


@pytest.fixture
def user(user_data, user_model):
    """Фикстура создает обычного активного пользователя."""
    return user_model.objects.create_user(**user_data)


@pytest.fixture
def superuser(superuser_data, user_model):
    """Фикстура создает администратора."""
    return user_model.objects.create_superuser(**superuser_data)


@pytest.fixture
def client():
    """Фикстура для создания клиента."""
    return Client()


@pytest.fixture
def api_client():
    return APIClient()
