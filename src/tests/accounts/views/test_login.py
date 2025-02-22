import pytest

from django.contrib.messages import get_messages


@pytest.mark.django_db
def test_login_view_get(client, login_url):
    """Проверяет, что GET-запрос возвращает страницу с формой."""
    response = client.get(login_url)

    assert response.status_code == 200
    assert "form" in response.context
    assert "accounts/login.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_login_view_post_valid_user(client, login_url, home_url, user_data, user):
    """Проверяет вход с корректными данными обычного пользователя."""
    response = client.post(login_url, user_data)

    assert response.status_code == 302
    assert response.url == home_url

    messages = list(get_messages(response.wsgi_request))
    assert any("Вы успешно вошли в систему" in str(message) for message in messages)


@pytest.mark.django_db
def test_login_view_post_valid_admin(client, login_url, home_url, superuser_data, superuser):
    """Проверяет вход администратора."""
    response = client.post(login_url, superuser_data)

    assert response.status_code == 302
    assert response.url == home_url

    messages = list(get_messages(response.wsgi_request))
    assert any("Вы являетесь администратором" in str(message) for message in messages)


@pytest.mark.django_db
def test_login_view_post_invalid_credentials(client, login_url):
    """Проверяет вход с некорректными данными."""
    response = client.post(login_url, {"email": "wrong@example.com", "password": "wrongpassword"})

    assert response.status_code == 302
    assert response.url == login_url

    messages = list(get_messages(response.wsgi_request))
    assert any(
        "Такого пользователя с такими данными не существует" in str(message) for message in messages
    )


@pytest.mark.django_db
def test_login_view_post_invalid_form(client, login_url):
    """Проверяет вход с некорректной формой."""
    response = client.post(login_url, {"email": "invalid_email", "password": ""})

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors
