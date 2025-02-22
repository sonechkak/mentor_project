from django import forms
from django.core.exceptions import ValidationError

from apps.accounts.validators import NotEmptyValidator
from apps.admin.validators import SlugValidator, LatinCyrillicValidator, MinMaxLengthValidator
from apps.blog.models import Category


class CategoryEditForm(forms.ModelForm):
    cat_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Category
        fields = ["cat_name", "slug", "is_draft"]

        widgets = {
            "is_draft": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_cat_name(self):
        cat_name = self.cleaned_data.get("cat_name")

        NotEmptyValidator().validate(cat_name)
        MinMaxLengthValidator(min_length=1, max_length=30).validate(cat_name)
        LatinCyrillicValidator().validate(cat_name)

        return cat_name

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")

        NotEmptyValidator().validate(slug)
        MinMaxLengthValidator(min_length=1, max_length=30).validate(slug)
        SlugValidator().validate(slug)

        if Category.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Категория с таким slug уже существует")

        return slug
