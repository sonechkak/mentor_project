import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import DetailView
from social_django.models import UserSocialAuth

from .forms import LoginForm, RegisterForm
from .utils import normalize_email

logger = logging.getLogger("accounts")


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
        is_google_connected = False
        extra_data = None

        # Проверяем подключение Google аккаунта
        try:
            google_login = UserSocialAuth.objects.get(user=request.user, provider="google-oauth2")
            is_google_connected = True
            extra_data_google = google_login.extra_data
        except UserSocialAuth.DoesNotExist:
            pass

        # Проверяем подключение GitHub аккаунта
        try:
            github_login = UserSocialAuth.objects.get(user=request.user, provider="github")
            extra_data_github = github_login.extra_data
            extra_data = github_login.extra_data  # для обратной совместимости
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
            "extra_data": extra_data,
            "is_google_connected": is_google_connected,
        }

        return render(request, self.template_name, context=context)


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        form_login = LoginForm()
        return render(
            request=request, template_name=self.template_name, context={"form": form_login}
        )

    def post(self, request):
        user_ip = request.META.get("REMOTE_ADDR")
        logger.info(f"POST запрос на страницу логина от {user_ip}")

        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            email = form_login.cleaned_data["email"]
            password = form_login.cleaned_data["password"]

            email = normalize_email(email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)

                logger.info(
                    f"Пользователь {user} с IP {user_ip} admin={user.is_admin}"
                    f"успешно аутентифицирован"
                )

                if user.is_active and not user.is_admin:
                    messages.success(
                        request,
                        "Вы успешно вошли в систему.\n" "Вы являетесь простым пользователем",
                    )

                if user.is_active and user.is_admin:
                    messages.success(
                        request, "Вы успешно вошли в систему.\n" "Вы являетесь администратором"
                    )

                return redirect("accounts:home")

            else:
                logger.warning(f"Неуспешная попытка входа для {email} с IP {user_ip}")
                messages.error(
                    request,
                    "Данные введены корректно.\n"
                    "Такого пользователя с такими данными не существует",
                )
                return redirect("accounts:login")

        logger.error(f"Ошибка валидации формы: "
                     f"{json.dumps(form_login.errors, ensure_ascii=False)}")
        return render(
            request=request, template_name=self.template_name, context={"form": form_login}
        )


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_ip = request.META.get("REMOTE_ADDR")

        logout(request)  # Завершаем сессию пользователя
        logger.info(f"Пользователь {user} с IP {user_ip} вышел из системы")
        return redirect("accounts:login")  # Перенаправляем на страницу логина


class RegisterView(View):
    template_name = "accounts/registration/register.html"

    def get(self, request):
        form_register = RegisterForm()
        return render(
            request=request, template_name=self.template_name, context={"form": form_register}
        )

    def post(self, request):
        user_ip = request.META.get("REMOTE_ADDR")
        logger.info(f"POST запрос на страницу регистрации от {user_ip}")

        form_register = RegisterForm(data=request.POST)
        if form_register.is_valid():
            try:
                user = form_register.save()
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                messages.success(request=request, message="Вы успешно зарегистрировались!")

                logger.info(
                    f"Пользователь {user} с IP {user_ip} admin={user.is_admin}"
                    f"успешно зарегистрирован."
                )
                return redirect("accounts:home")
            except Exception as e:
                logger.exception(f"Произошла ошибка при создании пользователя: {e}")

        logger.error(f"Ошибка валидации формы: "
                     f"{json.dumps(form_register.errors, ensure_ascii=False)}")
        return render(
            request=request, template_name=self.template_name, context={"form": form_register}
        )
