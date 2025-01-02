import logging

from django.contrib.auth import get_user_model

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, generics

from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.accounts.serializers import UserRegistrationSerializer, UserListSerializer
from apps.core.permissions.admin import IsSuperuserStaffAdmin

from apps.core.paginations.pagination_factory import get_pagination_class

User = get_user_model()
logger = logging.getLogger("accounts")


@extend_schema_view(
    post=extend_schema(
        summary="Регистрация нового пользователя в системе",
        tags=["Аутентификация & Авторизация"],
        operation_id="register user",
        request=UserRegistrationSerializer,
    ),
    get=extend_schema(
        summary="Получить список всех пользователей",
        tags=["Аутентификация & Авторизация"],
        operation_id="get all user",
        request=UserListSerializer,
    ),
)
class UserCreateAndRetrieveListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    pagination_class = get_pagination_class()

    def get(self, request, *args, **kwargs):
        """Метод для получения списка пользователей"""
        return super().get(request, *args, **kwargs)

    def post(self, request):
        """Метод для регистрации пользователя"""
        user_ip = request.META.get("REMOTE_ADDR")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
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

    def get_permissions(self):
        """Переопределяем get_permissions, чтобы использовать разные права доступа для POST и GET"""
        permissions = [AllowAny] if self.request.method == "POST" else [IsSuperuserStaffAdmin]
        self.permission_classes = permissions
        return super().get_permissions()

    def get_serializer_class(self):
        return UserRegistrationSerializer if self.request.method == "POST" else UserListSerializer
