from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .utils import normalize_email
from .validators import PASSWORD_VALIDATORS, NotEmptyValidator, NameValidator


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите Ваш Email"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите Ваш Пароль"}
        ),
    )


class RegisterForm(forms.ModelForm):
    User = get_user_model()

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Введите Имя"}),
        validators=[NotEmptyValidator(), NameValidator()],
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Введите Ваш Email"}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Введите Ваш Пароль"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите Пароль"})
    )

    class Meta:
        model = get_user_model()
        fields = ("first_name", "email")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs["class"] = "form-control"

    def clean_email(self):
        email = normalize_email(self.cleaned_data.get("email"))
        if self.User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        for validator in PASSWORD_VALIDATORS:
            try:
                validator()(password)
            except ValidationError as e:
                self.add_error("password1", e.message)
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        first_name = self.cleaned_data.get("first_name")
        email = normalize_email(self.cleaned_data.get("email"))
        password = self.cleaned_data.get("password2")

        if commit:
            user = self.User.objects.create_user(
                first_name=first_name,
                email=email,
                password=password,
            )
        else:
            user = self.User(first_name=first_name, email=email)
            user.set_password(password)
        return user
