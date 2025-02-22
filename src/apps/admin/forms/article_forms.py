from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput
from mdeditor.widgets import MDEditorWidget

from apps.blog.models import Category, Tag, Article
from apps.blog.validators.validators import (
    min_five_symbols_validator,
    article_image_validators,
)

User = get_user_model()


class ArticleForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Автор*",
        widget=forms.Select(attrs={"class": "input-author"}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Категории*",
        widget=forms.Select(attrs={"class": "input-category"}),
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    image = forms.FileField(
        label="Загрузите изображение",
        widget=forms.ClearableFileInput(attrs={"class": "d-none"}),
        validators=article_image_validators,
        required=False,
    )

    class Meta:
        model = Article

        fields = [
            "title",
            "slug",
            "image",
            "content",
            "published",
            "author",
            "category",
            "tags",
            "is_draft",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "input-title","placeholder": "Название*"}),
            "slug": forms.TextInput(attrs={"class": "input-slug", "placeholder": "Slug*"}),
            "content": MDEditorWidget(attrs={"class": "input-content", "placeholder": "Что будет в статье?"}),
            "published": DateTimeInput(attrs={"class": "datetimepicker"}),
            "is_draft": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


    def clean_title(self):
        title = self.cleaned_data.get("title")
        min_five_symbols_validator(title)
        return title


    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if self.instance.pk:
            if Article.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Такой slug уже существует. Выберите другой.")
        else:
            if Article.objects.filter(slug=slug).exists():
                raise ValidationError("Такой slug уже существует. Выберите другой.")
        return slug


    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content.strip()) < 1:
            raise ValidationError("Текст должен содержать минимум 1 символ.")
        return content


    def clean_tags(self):
        tags = self.cleaned_data.get("tags")
        if len(tags) < 1:
            raise ValidationError("Выберите минимум 1 тег.")
        if len(tags) > 6:
            raise ValidationError("Можно выбрать максимум 6 тегов.")
        return tags
