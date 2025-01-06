import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth import get_user_model

from apps.core.permissions import IsSuperuserStaffAdmin
from apps.core.mixins.paginations.mixins import PaginationMixin
from apps.admin.filters import SearchUserFilter


User = get_user_model()
logger = logging.getLogger("admin")


class ListUsersView(LoginRequiredMixin, UserPassesTestMixin, PaginationMixin, ListView):
    model = User
    template_name = "admin/list_users.html"
    ordering = ["id"]

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_admin=False)
        self.filter = SearchUserFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_users = super().get_queryset().filter(is_admin=False).count()
        context["total_users"] = total_users
        return context

    def test_func(self):
        permission = IsSuperuserStaffAdmin()
        has_permission = permission.has_permission(self.request)
        if not has_permission:
            logger.warning(f"Пользователю {self.request.user} отказано в доступе ")
        return has_permission

    def handle_no_permission(self):
        response = render(self.request, "403.html")
        response.status_code = 403
        return response
