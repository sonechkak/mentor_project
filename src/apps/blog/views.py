from django.views.generic import ListView

from .models import Article


class ArticleList(ListView):
    model = Article
    template_name = "blog/list.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.order_by("-date_publication")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Статьи"
        return context
