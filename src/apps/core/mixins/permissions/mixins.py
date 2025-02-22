import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render

from apps.core.permissions import IsSuperuserStaffAdmin

logger = logging.getLogger("admin")


class OnlyAdminAccessMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        permission = IsSuperuserStaffAdmin()
        has_permission = permission.has_permission(self.request)
        if not has_permission:
            logger.warning(f"Пользователю {self.request.user} отказано в доступе ")
        return has_permission

    def handle_no_permission(self):
        response = render(request=self.request, template_name="403.html")
        response.status_code = 403
        return response
