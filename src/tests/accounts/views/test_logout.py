import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_logout_view(client, user):
    """
    Проверяет, что после вызова LogoutView:
    1. Пользователь выходит из системы.
    2. Происходит редирект на страницу логина.
    """
    client.login(email="user@example.com", password="Userpassword123/*-")

    response = client.get(reverse("accounts:home"))
    assert response.wsgi_request.user.is_authenticated

    response = client.get(reverse("accounts:logout"))
    assert response.status_code == 302
    assert response.url == reverse("accounts:login")

    response = client.get(reverse("accounts:home"))
    assert not response.wsgi_request.user.is_authenticated
