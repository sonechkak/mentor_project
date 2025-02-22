from django.contrib.postgres.search import TrigramSimilarity, TrigramWordSimilarity
from django.db.models import Q, Count, CharField
from django.db.models.functions import Lower
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages
from django.db.models import Value

from apps.blog.forms import SearchForm, AddCommentForm
from apps.blog.models import Article, Tag, ArticleTag, Comment, Category


class ArticleListView(ListView):
    model = Article
    context_object_name = "articles"
    paginate_by = 5
    template_name = "blog/list.html"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("author", "category")
            .prefetch_related("tags")
        )

        # Фильтруем по категории (если передан cat_slug)
        cat_slug = self.kwargs.get("cat_slug")
        if cat_slug:
            queryset = queryset.filter(category__slug=cat_slug)

        # Фильтрация по поисковому запросу
        query = self.request.GET.get("query")
        if query:
            form = SearchForm(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data["query"]

                queryset = queryset.annotate(
                    title_sim=TrigramSimilarity(Lower("title"), Value(query.lower(), output_field=CharField())),
                    content_sim=TrigramSimilarity(Lower("content"), Value(query.lower(), output_field=CharField()))
                ).filter(
                    Q(title_sim__gt=0.1) | Q(content_sim__gt=0.1)
                ).order_by("-title_sim", "-content_sim")

        # Фильтрация по тегу
        tag_slug = self.request.GET.get("tag")
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        return queryset.distinct()  # distinct() нужен, чтобы избежать дублирования статей

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.published.all().annotate(total=Count("articles")).filter(total__gt=0) # Все опубликованные статьи, у которых есть хотя бы одна статья
        context["tags"] = Tag.published.all() # Все опубликованные теги

        # Выбранная категория
        cat_slug = self.kwargs.get("cat_slug")
        category = Category.published.filter(slug=cat_slug).first() if cat_slug else None
        context["cat_selected"] = category.id if category else 0
        context["cat_selected_slug"] = category.slug if category else None

        # Выбранный тег
        tag_slug = self.request.GET.get("tag")
        tag = Tag.published.filter(slug=tag_slug).first() if tag_slug else None
        context["tag_selected"] = tag.slug if tag else None

        # Передаем текущий поисковый запрос
        context["query"] = self.request.GET.get("query", "")

        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = "blog/detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.filter(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = AddCommentForm()
        context["parents_comments"] = self.object.comment.filter(parent_comment=None)
        context['cats'] = Category.published.all().annotate(total=Count("articles")).filter(total__gt=0)

        # Добавляем в контекст параметры фильтрации для использования в URL
        cat_slug = self.kwargs.get("cat_slug")
        category = Category.published.filter(slug=cat_slug).first() if cat_slug else None
        context["cat_selected"] = category.id if category else 0
        context["cat_selected_slug"] = category.slug if category else None
        context["cat_slug"] = self.request.GET.get("cat_slug")
        context["query"] = self.request.GET.get("query")
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

