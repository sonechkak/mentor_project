from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView

from accounts.models import User
from rapidfuzz.distance.Prefix import similarity

from .forms import SearchForm, AddCommentForm
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

        if self.request.GET.get("query"):
            form = SearchForm(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data["query"]
                queryset = queryset.annotate(
                    title_similarity=TrigramSimilarity("title", query),
                    content_similarity=TrigramSimilarity("content", query),
                ).filter(
                    Q(title_similarity__gt=0.3) | Q(content_similarity__gt=0.3)
                ).order_by("-title_similarity", "-content_similarity")
            else:
                form = SearchForm()
        if tag_slug:
            tag = Tag.objects.get(slug=tag_slug)
            queryset = queryset.filter(tags=tag)

        return queryset

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

class AddCommit(CreateView):
    form_class = AddCommentForm
    template_name = 'blog/add_commit.html'
    title_page = 'Добавление страницы'
    permission_required = 'women.add_women'

'''
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)
'''