import pytest

from django.contrib.auth import get_user_model
from django.test import Client


@pytest.fixture
def user_model():
    """Фикстура возращает модель User."""
    return get_user_model()


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
