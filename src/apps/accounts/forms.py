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
