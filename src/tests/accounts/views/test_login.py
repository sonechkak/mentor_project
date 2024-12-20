import pytest

from django.urls import reverse
from django.contrib.messages import get_messages


@pytest.mark.django_db
def test_login_view_get(client):
    """Проверяет, что GET-запрос возвращает страницу с формой."""
    response = client.get(reverse("accounts:login"))

    assert response.status_code == 200
    assert "form" in response.context
    assert "accounts/login.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_login_view_post_valid_user(client, user):
    """Проверяет вход с корректными данными обычного пользователя."""
    response = client.post(
        reverse("accounts:login"), {"email": "user@example.com", "password": "Userpassword123/*-"}
    )

    assert response.status_code == 302
    assert response.url == reverse("accounts:home")

    messages = list(get_messages(response.wsgi_request))
    assert any("Вы успешно вошли в систему" in str(message) for message in messages)


@pytest.mark.django_db
def test_login_view_post_valid_admin(client, superuser):
    """Проверяет вход администратора."""
    response = client.post(
        reverse("accounts:login"), {"email": "admin@example.com", "password": "Adminpassword123/*-"}
    )

    assert response.status_code == 302
    assert response.url == reverse("accounts:home")

    messages = list(get_messages(response.wsgi_request))
    assert any("Вы являетесь администратором" in str(message) for message in messages)


@pytest.mark.django_db
def test_login_view_post_invalid_credentials(client):
    """Проверяет вход с некорректными данными."""
    response = client.post(
        reverse("accounts:login"), {"email": "wrong@example.com", "password": "wrongpassword"}
    )

    assert response.status_code == 302
    assert response.url == reverse("accounts:login")

    messages = list(get_messages(response.wsgi_request))
    assert any(
        "Такого пользователя с такими данными не существует" in str(message) for message in messages
    )


@pytest.mark.django_db
def test_login_view_post_invalid_form(client):
    """Проверяет вход с некорректной формой."""
    response = client.post(reverse("accounts:login"), {"email": "invalid_email", "password": ""})

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors
