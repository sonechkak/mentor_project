# Generated by Django 4.2.16 on 2025-02-18 10:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import landing.models
import landing.utils
import landing.validators.img_param
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AboutMe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "text",
                    mdeditor.fields.MDTextField(
                        max_length=500,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Минимум 10 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                500, message="Максимум 500 символов"
                            ),
                        ],
                        verbose_name="Текст",
                    ),
                ),
            ],
            bases=(landing.models.MDTextFieldMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Content",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=40,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Минимум 10 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                40, message="Максимум 40 символов"
                            ),
                        ],
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=landing.utils.content_image_upload_to,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "svg", "png"]
                            ),
                            landing.validators.img_param.validate_content_image_size,
                        ],
                        verbose_name="Иконка",
                    ),
                ),
                (
                    "text",
                    mdeditor.fields.MDTextField(
                        max_length=500,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Минимум 10 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                500, message="Максимум 500 символов"
                            ),
                        ],
                        verbose_name="Описание",
                    ),
                ),
                ("link", models.URLField(verbose_name="Ссылка")),
                (
                    "link_text",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                1, message="Минимум 1 символ"
                            ),
                            django.core.validators.MaxLengthValidator(
                                100, message="Максимум 100 символов"
                            ),
                        ],
                        verbose_name="Текст ссылки",
                    ),
                ),
            ],
            bases=(landing.models.MDTextFieldMixin, models.Model),
        ),
        migrations.CreateModel(
            name="MainInf",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=50,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Минимум 10 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                50, message="Максимум 50 символов"
                            ),
                        ],
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "text",
                    mdeditor.fields.MDTextField(
                        max_length=500,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Минимум 10 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                500, message="Максимум 500 символов"
                            ),
                        ],
                        verbose_name="Текст",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=landing.utils.main_image_upload_to,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "svg", "png", "webp"]
                            ),
                            landing.validators.img_param.validate_main_image_size,
                        ],
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "telegram",
                    models.URLField(
                        blank=True,
                        max_length=40,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                5, message="Минимум 5 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                40, message="Максимум 40 символов"
                            ),
                        ],
                        verbose_name="Telegram",
                    ),
                ),
                (
                    "discord",
                    models.URLField(
                        blank=True,
                        max_length=40,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                5, message="Минимум 5 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                40, message="Максимум 40 символов"
                            ),
                        ],
                        verbose_name="Discord",
                    ),
                ),
                (
                    "vk",
                    models.URLField(
                        blank=True,
                        max_length=40,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                5, message="Минимум 5 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                40, message="Максимум 40 символов"
                            ),
                        ],
                        verbose_name="VK",
                    ),
                ),
            ],
            bases=(landing.models.MDTextFieldMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=40,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Минимум 10 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                40, message="Максимум 40 символов"
                            ),
                        ],
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "price",
                    models.IntegerField(
                        blank=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(999999),
                        ],
                        verbose_name="Цена",
                    ),
                ),
                (
                    "text",
                    mdeditor.fields.MDTextField(
                        max_length=500,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Минимум 10 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                500, message="Максимум 500 символов"
                            ),
                        ],
                        verbose_name="Описание",
                    ),
                ),
            ],
            bases=(landing.models.MDTextFieldMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Point",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        max_length=100,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                10, message="Минимум 10 символов"
                            ),
                            django.core.validators.MaxLengthValidator(
                                100, message="Максимум 100 символов"
                            ),
                        ],
                        verbose_name="Пункт",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="points",
                        to="landing.product",
                    ),
                ),
            ],
        ),
    ]
