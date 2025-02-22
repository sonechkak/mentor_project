from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from apps.accounts.validators import NotEmptyValidator
from apps.admin.validators import MinMaxLengthValidator, LatinCyrillicValidator, SlugValidator
from apps.blog.models import Tag
from apps.blog.validators.validators import validate_tag_icon_size, hex_color_validator


class TagEditForm(forms.ModelForm):
    tag_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    slug = forms.SlugField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    icon = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    color = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color"})
    )

    is_draft = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Tag
        fields = ["tag_name", "slug", "is_draft", "icon", "color"]

    def clean_tag_name(self):
        tag_name = self.cleaned_data.get("tag_name")

        NotEmptyValidator().validate(tag_name)
        MinMaxLengthValidator(min_length=1, max_length=30).validate(tag_name)
        LatinCyrillicValidator().validate(tag_name)

        if Tag.objects.filter(slug=tag_name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Тег с таким именем уже существует")

        return tag_name

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")

        NotEmptyValidator().validate(slug)
        MinMaxLengthValidator(min_length=1, max_length=30).validate(slug)
        SlugValidator().validate(slug)

        if Tag.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Тег с таким slug уже существует")

        return slug

    def clean_icon(self):
        icon = self.cleaned_data.get("icon")
        if icon:
            # Проверяем расширение файла
            FileExtensionValidator(allowed_extensions=["svg", "png"])(icon)
            # Проверяем размер изображения
            validate_tag_icon_size(icon)
        return icon

    def clean_color(self):
        color = self.cleaned_data.get("color")
        if color:
            hex_color_validator(color)
        return color

