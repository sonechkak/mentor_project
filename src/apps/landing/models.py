import markdown
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from mdeditor.fields import MDTextField

from landing.utils import main_image_upload_to, content_image_upload_to
from landing.validators.img_param import content_image_validators, main_image_validators
from apps.landing.validators.point_limit import max_seven_points_for_product


class MainInf(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Заголовок",
        validators=[
            MinLengthValidator(10, message="Минимум 10 символов"),
            MaxLengthValidator(50, message="Максимум 50 символов"), ]
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст',
        validators=[
            MinLengthValidator(10, message="Минимум 10 символов"),
            MaxLengthValidator(500, message="Максимум 500 символов"),
        ],
    )
    image = models.ImageField(
        upload_to=main_image_upload_to,
        verbose_name="Изображение",
        validators=main_image_validators,
    )
    telegram = models.URLField(
        max_length=40,
        verbose_name='Telegram',
        validators=[
            MinLengthValidator(5, message="Минимум 5 символов"),
            MaxLengthValidator(40, message="Максимум 40 символов"),
        ],
        blank=True,
    )
    discord = models.URLField(
        max_length=40,
        verbose_name='Discord',
        validators=[
            MinLengthValidator(5, message="Минимум 5 символов"),
            MaxLengthValidator(40, message="Максимум 40 символов"),
        ],
        blank=True,
    )
    vk = models.URLField(
        max_length=40,
        verbose_name='VK',
        validators=[
            MinLengthValidator(5, message="Минимум 5 символов"),
            MaxLengthValidator(40, message="Максимум 40 символов"),
        ],
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'landing'

class AboutMe(models.Model):
    text = MDTextField(
        max_length=500,
        verbose_name='Текст',
        validators=[
            MinLengthValidator(10, message="Минимум 10 символов"),
            MaxLengthValidator(500, message="Максимум 500 символов"),
        ],
    )

    def __str__(self):
        return self.text[:20]

    def text_html(self):
        return markdown.markdown(str(self.text), extensions=['extra', 'codehilite'])


class Content(models.Model):
    title = models.CharField(
        max_length=40,
        verbose_name="Заголовок",
        validators=[
        MinLengthValidator(10, message="Минимум 10 символов"),
        MaxLengthValidator(40, message="Максимум 40 символов"),]
    )
    image = models.ImageField(
        upload_to=content_image_upload_to,
        verbose_name="Иконка",
        validators=content_image_validators,
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Описание',
        validators=[
            MinLengthValidator(10, message="Минимум 10 символов"),
            MaxLengthValidator(500, message="Максимум 500 символов"),
        ],
    )
    link = models.URLField(verbose_name="Ссылка")
    link_text = models.CharField(
        max_length=100,
        verbose_name="Текст ссылки",
        validators=[
            MinLengthValidator(1, message="Минимум 1 символ"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        ],
    )

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(
        max_length=40,
        verbose_name="Заголовок",
        validators=[
        MinLengthValidator(10, message="Минимум 10 символов"),
        MaxLengthValidator(40, message="Максимум 40 символов"),]
    )
    price = models.IntegerField(
        verbose_name= 'Цена',
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999999)],
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Описание',
        validators=[
            MinLengthValidator(10, message="Минимум 10 символов"),
            MaxLengthValidator(500, message="Максимум 500 символов"),
        ],
    )

    def __str__(self):
        return self.title


class Point(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='points'
    )
    text = models.TextField(
        max_length=100,
        verbose_name='Пункт',
        validators=(
            MinLengthValidator(10, message="Минимум 10 символов"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        )
    )

    def __str__(self):
        return self.text[:20]

    def clean(self):
        # Проверяем, сколько пунктов уже связано с этим продуктом
        max_seven_points_for_product(self.product)
        return super().clean()