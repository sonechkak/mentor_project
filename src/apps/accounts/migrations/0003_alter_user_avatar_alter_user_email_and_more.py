# Generated by Django 4.2.16 on 2025-01-06 07:44

import accounts.utils
import accounts.validators.validators_user_model
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_avatar_alter_user_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                upload_to=accounts.utils.avatar_upload_to,
                validators=[accounts.validators.validators_user_model.ImageValidator.validate],
                verbose_name="Аватар",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254,
                unique=True,
                validators=[
                    accounts.validators.validators_user_model.NotEmptyValidator.validate,
                    accounts.validators.validators_user_model.EmailValidator.validate,
                ],
                verbose_name="Email",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                validators=[
                    accounts.validators.validators_user_model.NotEmptyValidator.validate,
                    accounts.validators.validators_user_model.NameValidator.validate,
                ],
                verbose_name="Имя",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                blank=True,
                validators=[
                    accounts.validators.validators_user_model.NotEmptyValidator.validate,
                    accounts.validators.validators_user_model.NameValidator.validate,
                ],
                verbose_name="Фамилия",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(
                validators=[
                    accounts.validators.validators_user_model.NotEmptyValidator.validate,
                    accounts.validators.validators_user_model.MinimumLengthValidator.validate,
                    accounts.validators.validators_user_model.UppercaseLetterValidator.validate,
                    accounts.validators.validators_user_model.NumericCharacterValidator.validate,
                    accounts.validators.validators_user_model.SpecialSymbolValidator.validate,
                ],
                verbose_name="Пароль",
            ),
        ),
    ]
