from django.contrib.auth.forms import UserCreationForm
from .models import User


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
            'is_staff',
            'is_superuser'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ваше имя'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ваша фамилия'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Ваш Email'})
        self.fields['is_staff'].label = 'Администратор'
        self.fields['is_superuser'].label = 'Суперпользователь'
