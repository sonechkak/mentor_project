# Generated by Django 4.2.16 on 2025-02-09 23:02

import accounts.validators.validators_user_model
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(
                validators=[
                    accounts.validators.validators_user_model.NotEmptyValidator.validate,
                    accounts.validators.validators_user_model.MinMaxLengthPasswordValidator.validate,
                    accounts.validators.validators_user_model.UppercaseLetterValidator.validate,
                    accounts.validators.validators_user_model.NumericCharacterValidator.validate,
                    accounts.validators.validators_user_model.SpecialSymbolValidator.validate,
                ],
                verbose_name="Пароль",
            ),
        ),
    ]
