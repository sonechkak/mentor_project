from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsSuperuserStaffAdmin(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        """
        Проверяем, что пользователь аутентифицирован и явл. администратором
        """
        return (
            getattr(request.user, "is_authenticated", False) and
            getattr(request.user, "is_superuser", False) and
            getattr(request.user, "is_staff", False) and
            getattr(request.user, "is_admin", False)
        )
