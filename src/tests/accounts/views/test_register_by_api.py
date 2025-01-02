import pytest

from rest_framework import status


@pytest.mark.django_db
class TestUserCreateAndRetrieveListView:
    def test_user_registration_success(
        self, api_client, user_data_valid_for_serializer, user_model
    ):
        """Тест на успешную регистрацию пользователя"""

        url = "/api/v1/users/"
        response = api_client.post(url, user_data_valid_for_serializer, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "success"
        assert response.data["message"] == "Пользователь успешно зарегистрирован."
        assert user_model.objects.filter(email=user_data_valid_for_serializer["email"]).exists()

    def test_user_registration_failure(self, api_client):
        """Тест на не успешную регистрацию пользователя"""

        url = "/api/v1/users/"
        user_data_invalid_for_serializer = {
            "first_name": "",
            "email": "invalid email",
            "password": "short",
        }
        response = api_client.post(url, user_data_invalid_for_serializer, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "error"
        assert "first_name" in response.data["errors"]
        assert "email" in response.data["errors"]
        assert "password" in response.data["errors"]
