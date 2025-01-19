from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .utils import normalize_email
from apps.accounts.validators import ImageValidator


class UserEditForm(forms.ModelForm):
    User = get_user_model()

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_admin",
            "avatar",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_admin": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "avatar": forms.ClearableFileInput(),
        }

    def clean_email(self):
        email = normalize_email(self.cleaned_data.get("email"))
        if self.User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            ImageValidator().validate(avatar)
        return avatar
