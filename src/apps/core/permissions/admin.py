from apps.core.permissions.base import CustomPermission
from apps.core.permissions.settings import settings


class IsSuperuserStaffAdmin(CustomPermission):
    """
    Проверка прав на основе ADMIN_PERMISSIONS из settings.py.
    """

    required_permissions = getattr(settings, "ADMIN_PERMISSIONS", [])
