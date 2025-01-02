import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.core.permissions import IsSuperuserStaffAdmin

User = get_user_model()
logger = logging.getLogger("admin")


class ListUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "admin/list_users.html"
    ordering = ["id"]

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search", "").strip()
        if search_query:
            # Фильтруем по имени, фамилии или email
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(email__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_size = self.request.GET.get("page_size", 10)  # Значение по умолчанию - 10
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = 10

        paginator = Paginator(self.get_queryset(), page_size)

        # Получаем номер страницы из GET-параметра или задаём 1 по умолчанию
        page_number = self.request.GET.get("page", 1)
        try:
            page_number = int(page_number)
            if page_number < 1:
                page_number = 1  # если номер страницы меньше 1, то используем 1
        except ValueError:
            page_number = 1  # если номер страницы не является целым числом, то используем 1

        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            # Если страница пуста, возвращаем последнюю страницу
            page_obj = paginator.get_page(paginator.num_pages)

        context["page_obj"] = page_obj
        context["page_size"] = page_size
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
