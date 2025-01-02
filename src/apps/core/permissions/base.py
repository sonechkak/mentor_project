from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class CustomPermission(BasePermission):
    """
    Универсальный класс проверки прав с использованием настроек.
    """

    required_permissions = []

    def has_permission(self, request: Request, view: View = None) -> bool:
        """
        Проверяем права пользователя на основе указанных required_permissions.
        """
        return all(getattr(request.user, perm, False) for perm in self.required_permissions)
