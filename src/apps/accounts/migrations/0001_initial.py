# Generated by Django 4.2.16 on 2024-12-07 08:33

import accounts.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2, 'Поле должно содержать минимум 2 символа.'), django.core.validators.RegexValidator(message='Поле может содержать только буквы латиницы и кириллицы.', regex='^[a-zA-Zа-яА-ЯёЁ]+$')])),
                ('last_name', models.CharField(blank=True, max_length=30, validators=[django.core.validators.MinLengthValidator(2, 'Поле должно содержать минимум 2 символа.'), django.core.validators.RegexValidator(message='Поле может содержать только буквы латиницы и кириллицы.', regex='^[a-zA-Zа-яА-ЯёЁ]+$')])),
                ('email', models.EmailField(error_messages={'invalid': 'Введите правильный адрес электронной почты.'}, max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message='Email должен содержать только буквы латиницы, цифры, спец. символы, но без пробелов.', regex='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')])),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(8, 'Пароль должен содержать минимум 8 символов.'), django.core.validators.RegexValidator(message='Пароль должен содержать хотя бы одну заглавную букву.', regex='[A-Z]'), django.core.validators.RegexValidator(message='Пароль должен содержать хотя бы одну цифру.', regex='\\d'), django.core.validators.RegexValidator(message='Пароль должен содержать хотя бы один спец. символ.', regex='[!@#$%^&*(),.?":{}|<>]')])),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=accounts.models.avatar_upload_to, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png']), accounts.models.validate_image_size])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
