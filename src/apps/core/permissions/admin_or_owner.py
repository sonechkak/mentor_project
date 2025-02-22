from rest_framework.permissions import BasePermission

from apps.core.permissions.settings import settings


class IsAdminOrOwner(BasePermission):
    """
    Проверка прав
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        is_admin = all(getattr(request.user, perm, False) for perm in settings.ADMIN_PERMISSIONS)
        return is_admin or obj == request.user
