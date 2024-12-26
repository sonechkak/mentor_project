import pytest


def test_register_view_get(client, register_url):
    """Проверяет, что GET-запрос возвращает страницу регистрации с формой."""
    response = client.get(register_url)

    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_register_view_post_valid_registration(client, register_url, home_url, user_model):
    """Тест успешной регистрации."""
    data = {
        "first_name": "User",
        "email": "user@example.com",
        "password1": "Userpassword123/*-",
        "password2": "Userpassword123/*-",
    }
    response = client.post(register_url, data)

    assert response.status_code == 302
    assert response.url == home_url
    assert user_model.objects.filter(email=data["email"]).exists()


@pytest.mark.django_db
def test_register_view_post_invalid_data(client, register_url):
    """Тест регистрации с некорректными данными."""
    data = {
        "first_name": "",
        "email": "invalid-email",
        "password1": "short",
        "password2": "differentpassword",
    }
    response = client.post(register_url, data)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors
