from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status, generics

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiTypes

from apps.accounts.serializers import (
    UserSerializer,
    UserChangePasswordSerializer,
    UserUpdateSerializer,
)
from apps.core.permissions import IsSuperuserStaffAdmin, IsAdminOrOwner, AllowOnlyNotAuthenticated
from apps.core.paginations.pagination_factory import get_pagination_class
from apps.core.decorators import log_request_operations

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary="Регистрация нового пользователя в системе",
        tags=["Accounts"],
        operation_id="register user",
        request=UserSerializer,
    ),
    get=extend_schema(
        summary="Получить список всех пользователей",
        tags=["Accounts"],
        operation_id="get all users",
        request=UserSerializer,
    ),
)
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    pagination_class = get_pagination_class()
    http_method_names = ["get", "post"]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """Метод для получения списка пользователей"""
        return super().list(request, *args, **kwargs)

    @log_request_operations(logger_name="accounts")
    def post(self, request, *args, **kwargs):
        """Метод для регистрации пользователя"""

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"status": "success", "message": "Пользователь успешно зарегистрирован."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_permissions(self):
        """Переопределяем get_permissions, чтобы использовать разные права доступа для POST и GET"""
        permissions = [AllowOnlyNotAuthenticated | IsSuperuserStaffAdmin] \
            if self.request.method == "POST" else \
            [IsSuperuserStaffAdmin]
        self.permission_classes = permissions
        return super().get_permissions()


@extend_schema_view(
    get=extend_schema(
        summary="Получение данных пользователя по ID",
        tags=["Accounts"],
        operation_id="get user data by ID",
        request=UserSerializer,
    ),
    put=extend_schema(
        summary="Обновление данных пользователя по ID",
        tags=["Accounts"],
        operation_id="update user data by ID",
        request=UserUpdateSerializer,
    ),
    delete=extend_schema(
        summary="Удаление данных пользователя по ID",
        tags=["Accounts"],
        operation_id="delete user by ID",
        request=None,
        responses={204: OpenApiTypes.NONE},
    ),
)
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    http_method_names = ["get", "put", "delete"]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @log_request_operations(logger_name="accounts")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @log_request_operations(logger_name="accounts")
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserUpdateSerializer(
            instance=instance,
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def get_permissions(self):
        """Переопределяем get_permissions, чтобы использовать разные права доступа для POST и GET"""
        permissions = [IsAdminOrOwner] if self.request.method in ("GET", "PUT") else [
            IsSuperuserStaffAdmin]
        self.permission_classes = permissions
        return super().get_permissions()


@extend_schema_view(
    patch=extend_schema(
        summary="Обновление пароля пользователя по id",
        tags=["Accounts"],
        operation_id="update password",
        request=UserChangePasswordSerializer,
    )
)
class UserChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsSuperuserStaffAdmin]
    lookup_field = "id"
    http_method_names = ["patch"]

    @log_request_operations(logger_name="accounts")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
