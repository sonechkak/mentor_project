from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages

from accounts.models import User
from rapidfuzz.distance.Prefix import similarity

from .forms import SearchForm, AddCommentForm
from .models import Tag, Comment
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
        context["comment_form"] = AddCommentForm()
        context["parents_comments"] = self.object.comment.filter(parent_comment=None)
        return context

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.increment_views(self.request)
        return obj

class BaseCommentView:
    model = Comment

    def get_success_url(self):
        # Получаем статью из текущего комментария и возвращаем на её детальную страницу
        article = Article.objects.get(pk=self.object.article.pk)
        return reverse(
            "blog:article_detail",
            kwargs={"slug": article.slug},
        )


class AddCommentView(BaseCommentView, CreateView):
    form_class = AddCommentForm
    template_name = "add_comment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаём None как значение родительского комментария по умолчанию
        context["parent_comment"] = None
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            # Создаем объект комментария, не сохраняя его в базу
            comment = form.save(commit=False)
            comment.author = self.request.user
            # Устанавливаем статью для комментария
            comment.article = Article.objects.get(slug=self.kwargs.get("slug"))

            # Проверяем, есть ли parent_comment_id в запросе
            parent_comment_id = self.request.POST.get("parent_comment_id")
            if parent_comment_id:
                try:
                    # Устанавливаем родительский комментарий, если он существует
                    comment.parent_comment = Comment.objects.get(pk=parent_comment_id)
                except Comment.DoesNotExist:
                    messages.error(self.request, "Родительский комментарий не найден.")
                    return redirect(self.get_success_url())

            # Сохраняем комментарий в базу
            comment.save()
            return super().form_valid(form)
        else:
            messages.error(self.request, "Пожалуйста, войдите в систему.")
            return redirect("accounts:login")