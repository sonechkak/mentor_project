from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import DetailView

from social_django.models import UserSocialAuth

from apps.accounts.forms import LoginForm, RegisterForm
from apps.accounts.utils import normalize_email
from apps.core.decorators.decorators import log_request_operations


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name)


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "accounts/profile.html"
    login_url = reverse_lazy("accounts:login")

    def get(self, request):
        # Инициализируем переменные значениями по умолчанию
        extra_data_google = None
        extra_data_github = None
        extra_data_vk = None
        extra_data_telegram = None
        extra_data = None

        # Проверяем подключение Google аккаунта
        try:
            google_login = UserSocialAuth.objects.filter(
                user=request.user, provider="google-oauth2"
            ).first()
            if google_login:
                extra_data_google = google_login.extra_data
        except UserSocialAuth.DoesNotExist:
            pass

        # Проверяем подключение GitHub аккаунта
        try:
            github_login = UserSocialAuth.objects.filter(
                user=request.user, provider="github"
            ).first()
            if github_login:
                extra_data_github = github_login.extra_data
        except UserSocialAuth.DoesNotExist:
            pass

        try:
            vk_login = UserSocialAuth.objects.filter(
                user=request.user, provider="vk-oauth2"
            ).first()
            if vk_login:
                extra_data_vk = vk_login.extra_data
        except UserSocialAuth.DoesNotExist:
            pass

        try:
            telegram_login = UserSocialAuth.objects.filter(
                user=request.user, provider="telegram"
            ).first()
            if telegram_login:
                extra_data_telegram = telegram_login.extra_data
        except UserSocialAuth.DoesNotExist:
            pass

        context = {
            "username": request.user.username,
            "full_name": f"{request.user.first_name} {request.user.last_name}",
            "email": request.user.email,
            "registration_date": request.user.date_joined.strftime("%d.%m.%Y"),
            "last_login": request.user.last_login.strftime("%d.%m.%Y %H:%M"),
            "is_active": request.user.is_active,
            "extra_data_google": extra_data_google,
            "extra_data_github": extra_data_github,
            "extra_data_vk": extra_data_vk,
            "extra_data_telegram": extra_data_telegram,
            "extra_data": extra_data,
        }

        return render(request, self.template_name, context=context)


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        form_login = LoginForm()
        return render(
            request=request, template_name=self.template_name, context={"form": form_login}
        )

    @log_request_operations(logger_name="accounts")
    def post(self, request):
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            email = form_login.cleaned_data["email"]
            password = form_login.cleaned_data["password"]

            email = normalize_email(email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)

                if user.is_active and not user.is_admin:
                    messages.success(
                        request,
                        "Вы успешно вошли в систему.\n" "Вы являетесь простым пользователем",
                    )

                if user.is_active and user.is_admin:
                    messages.success(
                        request, "Вы успешно вошли в систему.\n" "Вы являетесь администратором"
                    )

                return redirect("landing:home")

            else:
                messages.error(
                    request,
                    "Данные введены корректно.\n"
                    "Такого пользователя с такими данными не существует",
                )
                return redirect("accounts:login")

        return render(
            request=request, template_name=self.template_name, context={"form": form_login}
        )


class LogoutView(View):
    @log_request_operations(logger_name="accounts")
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:login")  # Перенаправляем на страницу логина


class RegisterView(View):
    template_name = "accounts/registration/register.html"

    def get(self, request, *args, **kwargs):
        form_register = RegisterForm()
        return render(
            request=request, template_name=self.template_name, context={"form": form_register}
        )

    @log_request_operations(logger_name="accounts")
    def post(self, request, *args, **kwargs):
        form_register = RegisterForm(data=request.POST)
        if form_register.is_valid():
            user = form_register.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request=request, message="Вы успешно зарегистрировались!")
            return redirect("landing:home")
        return render(
            request=request, template_name=self.template_name, context={"form": form_register}
        )
