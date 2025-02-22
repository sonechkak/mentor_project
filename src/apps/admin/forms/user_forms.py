from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from admin.utils import normalize_email
from apps.accounts.validators import ImageValidator, PASSWORD_VALIDATORS


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
            "first_name": forms.TextInput(attrs={"class": "name-input"}),
            "last_name": forms.TextInput(attrs={"class": "name-input"}),
            "email": forms.EmailInput(attrs={"class": "name-input"}),
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
            ImageValidator(["jpg", "png"]).validate(avatar)
        return avatar

    def save(self, commit=True):
        instance = super().save(commit=False)
        is_admin = self.cleaned_data.get("is_admin")

        instance.is_superuser = is_admin
        instance.is_staff = is_admin

        if commit:
            instance.save()
        return instance


class UserCreateForm(UserEditForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "name-input"}),
    )
    

    def clean_email(self):
        email = normalize_email(self.cleaned_data.get("email"))
        if self.User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        for validator in PASSWORD_VALIDATORS:
            try:
                validator()(password)
            except ValidationError as e:
                self.add_error("password", e.message)
        return password

    def save(self, commit=True):
        first_name = self.cleaned_data.pop("first_name")
        email = normalize_email(self.cleaned_data.pop("email"))
        password = self.cleaned_data.pop("password")

        extra_fields = dict(self.cleaned_data.items())
        extra_fields["is_staff"] = extra_fields["is_admin"]
        extra_fields["is_superuser"] = extra_fields["is_admin"]

        if commit:
            user = self.User.objects.create_user(
                first_name=first_name,
                email=email,
                password=password,
                **extra_fields,
            )
        else:
            user = self.User(first_name=first_name, email=email, **extra_fields)
            user.set_password(password)
        return user

