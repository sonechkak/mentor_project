import logging

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.accounts.serializers import UserRegistrationSerializer

logger = logging.getLogger("accounts")


@extend_schema_view(
    post=extend_schema(
        summary="Регистрация нового пользователя в системе",
        tags=["Аутентификация & Авторизация"],
        operation_id="register user",
        request=UserRegistrationSerializer,
    )
)
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user_ip = request.META.get("REMOTE_ADDR")
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                logger.info(
                    f"Пользователь {user} с IP {user_ip} admin={user.is_admin}"
                    f" успешно зарегистрирован."
                )
                return Response(
                    data={"status": "success", "message": "Пользователь успешно зарегистрирован."},
                    status=status.HTTP_201_CREATED,
                )
            logger.error(f"Ошибка валидации: {serializer.errors}")
            return Response(
                data={"status": "error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Внутренняя ошибка сервера: {e}")
            return Response(
                data={"status": "error", "message": "Внутренняя ошибка сервера."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
