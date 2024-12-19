from django import forms

from apps.accounts.validators.validators_user_model import (
    email_validator,
    password_validators,
)


class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        validators=[email_validator],
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        validators=password_validators,
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
