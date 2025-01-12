from django.views.generic import ListView, DetailView

from accounts.models import User
from .models import Tag
from .models import Article


class ArticleListView(ListView):
    model = Article
    context_object_name = "articles"
    paginate_by = 5
    template_name = "blog/list.html"

    def get_queryset(self):
        queryset = (super().get_queryset().select_related("author").prefetch_related("tags",))
        tag_slug = self.kwargs.get("slug")
        if tag_slug:
            tag = Tag.objects.get(slug=tag_slug)
            queryset = queryset.filter(tags=tag)

        return queryset.order_by("-published")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["superuser"] = User.objects.filter(is_superuser=True).first()
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = "blog/detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.filter(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = self.object.tags.all()
        context["superuser"] = User.objects.filter(is_superuser=True).first()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.increment_views(self.request)
        return obj


class ArticleByTag(ArticleListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        tag = Tag.objects.get(slug=self.kwargs["slug"])
        return queryset.filter(tags=tag).order_by("-published")
