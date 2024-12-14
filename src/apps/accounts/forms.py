from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from .validators.validators_user_model import email_validator, password_validators


class LoginForm(forms.Form):
    email = forms.EmailField(
        validators=[email_validator],
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            "placeholder": "Введите Ваш Email"
        })
    )
    password = forms.CharField(
        validators=password_validators,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            "placeholder": "Введите Ваш Пароль"
        })
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'avatar',
            "is_active",
            'is_staff',
            'is_superuser',
            "is_admin"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ваше имя'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ваша фамилия'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Ваш Email'})
        self.fields['is_active'].label = 'Активный пользователь поле is_active (Django field)'
        self.fields['is_staff'].label = 'Администратор поле is_staff (Django field)'
        self.fields['is_superuser'].label = 'Суперпользователь поле is_superuser (Django field)'
        self.fields['is_admin'].label = 'Наше кастомное поле для is_admin'
