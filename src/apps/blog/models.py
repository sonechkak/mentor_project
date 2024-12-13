from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet, Manager
from django.urls import reverse

from .utils import article_image_upload_to, tag_icon_upload_to
from .validators.validators_blog_models import (
    title_validators,
    slug_validators,
    article_image_validators,
    content_validators,
    name_validators,
    tag_icon_validators,
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
        DRAFT = 1, 'Черновик'
        PUBLISHED = 0, 'Опубликовано'

    is_draft = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.PUBLISHED,
        verbose_name='Черновик'
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True


class Article(PublishableModel):
    title = models.CharField(
        max_length=40,
        verbose_name='Название',
        validators=title_validators
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Slug',
        validators=slug_validators
    )
    # ?add later class ArticleAdmin(admin.ModelAdmin): prepopulated_fields = {"slug": ["title"]}
    image = models.ImageField(
        upload_to=article_image_upload_to,
        default=None,
        blank=True,
        null=True,
        verbose_name='Изображение',
        validators=article_image_validators
    )
    content = models.TextField(       # need to change on MarkdownxField()
        verbose_name='Текст',
        validators=content_validators
    )
    date_publication = models.DateTimeField(
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        get_user_model(), # изменить, подумать и обсудить, что здесь должно быть
        on_delete=models.SET_DEFAULT,
        related_name='article',
        null=True,
        default=None # поменять на какую-то фразу об удаленном авторе
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='article',
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='article',
        verbose_name='Теги'
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-date_publication']
        indexes = [
            models.Index(fields=['-date_publication'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})


class Category(PublishableModel):
    cat_name = models.CharField(
        max_length=30,
        db_index=True,
        verbose_name='Категория',
        validators=name_validators
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        validators=slug_validators
    )


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.cat_name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Tag(PublishableModel):
    tag_name = models.CharField(
        max_length=30,
        db_index=True,
        validators=name_validators
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        validators=slug_validators
    )
    icon = models.ImageField(
        upload_to=tag_icon_upload_to,
        verbose_name='Иконка',
        validators=tag_icon_validators
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})