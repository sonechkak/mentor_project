from rest_framework.permissions import BasePermission


class AllowOnlyNotAuthenticated(BasePermission):
    """
    Разрешает доступ только НЕ аутентифицированным пользователям.
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated
