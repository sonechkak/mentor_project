from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserCreationForm
    model = User

    # Устанавливаем поля, которые будут отображаться в списке пользователей
    list_display = ['first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['email']

    # Поля, которые будут отображаться при добавлении и редактировании пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'avatar',
                'is_staff',
                'is_superuser'),
        }),
    )
