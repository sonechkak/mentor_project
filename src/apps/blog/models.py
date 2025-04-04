import markdown
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import QuerySet, Manager, F
from django.urls import reverse
from django.utils import timezone
from mdeditor.fields import MDTextField
from .utils import article_image_upload_to, tag_icon_upload_to
from .validators.validators import (
    slug_validators,
    min_five_symbols_validator,
    min_one_symbol_validator,
    article_image_validators,
    tag_icon_validators, hex_color_validator,
)


class PublishableQuerySet(QuerySet):
    """Подкласс QuerySet, который добавляет метод published() для отбора опубликованных записей,
    без статуса черновика"""

    def published(self):
        return self.filter(is_draft=False)


class PublishedManager(Manager.from_queryset(PublishableQuerySet)):
    """Менеджер, использующий наш PublishableQuerySet. Он переопределяет метод get_queryset:
    он возвращает только опубликованные записи."""

    def get_queryset(self):
        return super().get_queryset().published()


class PublishableModel(models.Model):
    """Абстрактная модель, содержащая общее для всех моделей поле is_draft, менеджеры objects (стандартный)
    и published (возвращает только опубликованные записи модели, без статуса черновика). Например,
    для отбора всех опубликованных статей используем: Article.published.all()"""

    class Status(models.IntegerChoices):
        DRAFT = 1, "Черновик"
        PUBLISHED = 0, "Опубликовано"

    is_draft = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.PUBLISHED,
        verbose_name="Черновик",
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True


class Tag(PublishableModel):
    tag_name = models.CharField(
        max_length=30, db_index=True, validators=(min_one_symbol_validator,)
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        validators=slug_validators,
    )
    icon = models.ImageField(
        upload_to=tag_icon_upload_to,
        verbose_name="Иконка",
        validators=tag_icon_validators,
        null=True,
        blank=True,
    )
    color = models.CharField(
        max_length=7,
        default="#838DD1",
        validators=[hex_color_validator,],
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        app_label = 'blog'

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return reverse("admin:edit-tag", kwargs={"slug": self.slug})


class Category(PublishableModel):
    cat_name = models.CharField(
        max_length=30,
        db_index=True,
        verbose_name="Категория",
        validators=(min_one_symbol_validator,),
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        validators=slug_validators,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.cat_name

    def get_absolute_url(self):
        return reverse("admin:category-edit", kwargs={"cat_slug": self.slug})


class Article(PublishableModel):
    title = models.CharField(
        max_length=40, verbose_name="Название", validators=(min_five_symbols_validator,)
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name="Slug",
        validators=slug_validators,
    )
    image = models.ImageField(
        upload_to=article_image_upload_to,
        default=None,
        blank=True,
        null=True,
        verbose_name="Изображение",
        validators=article_image_validators,
    )
    content = MDTextField(verbose_name="Текст", validators=(min_one_symbol_validator,))

    published = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="articles",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="articles",
        verbose_name="Категория",
    )
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    tags = models.ManyToManyField(Tag, through='ArticleTag', related_name="articles_new")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-published"]
        indexes = [models.Index(fields=["-published"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article", kwargs={"slug": self.slug})

    def increment_views(self, request):
        # Ключ для хранения просмотренных статей в сессии
        viewed_articles = request.session.get("viewed_articles", [])

        # Проверяем, был ли уже просмотрен этот объект (чтобы не засчитывать повторные просмотры)
        if self.id not in viewed_articles:
            # Увеличиваем количество просмотров на 1 с помощью `F("views") + 1`
            self.__class__.objects.filter(pk=self.pk).update(views=F("views") + 1)

            # Добавляем текущий ID статьи в список просмотренных
            viewed_articles.append(self.id)

            # Обновляем сессию пользователя
            request.session["viewed_articles"] = viewed_articles

    def content_html(self):
        return markdown.markdown(str(self.content), extensions=['extra', 'codehilite'])

class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)  # Поле для хранения порядка тегов

    class Meta:
        ordering = ['order']  # Сортировка по порядку

    def __str__(self):
        return f"Статья {self.article} - тег {self.tag}"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="comment",
        null=True,
        blank=True,
    )
    html_content = models.TextField(
        max_length=500, verbose_name="Текст", validators=(min_one_symbol_validator,)
    )
    date_publication = models.DateTimeField(verbose_name="Дата публикации", default= timezone.now)
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.SET_DEFAULT,
        null=True,
        blank=True,
        related_name="replies",
        default=None,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["date_publication"]

    def __str__(self):
        return f"Комментарий {self.author}: {self.html_content[:50]}"

    def get_child_comments(self):
        return Comment.objects.filter(parent_comment=self)
