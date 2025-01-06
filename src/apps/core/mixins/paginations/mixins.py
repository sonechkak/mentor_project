from django.core.paginator import Paginator, EmptyPage


class PaginationMixin:
    """Миксин для добавления пагинации в контекст."""
    page_size = 20  # Значение по умолчанию

    def _get_page_size(self):
        """Получает значение параметра пагинации из запроса или возвращает значение по умолчанию."""
        page_size = self.request.GET.get("page_size", self.page_size)
        if page_size == "all":
            return None
        try:
            return int(page_size)
        except ValueError:
            return self.page_size

    def _paginate_queryset(self, queryset):
        """Пагинирует queryset на основе параметров."""
        page_size = self._get_page_size()
        if page_size is None:  # Если page_size == None, возвращаем весь queryset
            return queryset, None

        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get("page", 1)
        try:
            page_number = int(page_number)
            if page_number < 1:
                page_number = 1
        except ValueError:
            page_number = 1

        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        return page_obj.object_list, page_obj

    def get_context_data(self, **kwargs):
        """Добавляет объекты пагинации в контекст."""
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        object_list, page_obj = self._paginate_queryset(queryset)
        page_size = self._get_page_size()
        context["page_size"] = page_size
        context["page_obj"] = page_obj
        context["object_list"] = object_list
        return context
