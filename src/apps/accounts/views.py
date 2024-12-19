from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import LoginForm
from .utils import normalize_email


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        form_login = LoginForm()
        return render(
            request=request,
            template_name=self.template_name,
            context={"form": form_login},
        )

    def post(self, request):
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            email = form_login.cleaned_data["email"]
            password = form_login.cleaned_data["password"]

            email = normalize_email(email)
            # Аутентификация пользователя
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active and not user.is_admin:
                    # Проверка на активность и что пользователь не администратор
                    print("-----------DO NOT ADMIN-----------")
                    login(request, user)
                    messages.success(
                        request,
                        "Вы успешно вошли в систему.\n"
                        "Вы являетесь простым пользователем",
                    )
                    return redirect(
                        "accounts:home"
                    )  # Редирект для простого пользователя

                if user.is_active and user.is_admin:
                    # Проверка на активность и что пользователь явл. администратор
                    print("-----------ADMIN-----------")
                    login(request, user)
                    messages.success(
                        request,
                        "Вы успешно вошли в систему.\n" "Вы являетесь администратором",
                    )
                    return redirect("accounts:home")  # Редирект для успешного входа
            else:
                messages.error(
                    request,
                    "Данные введены корректно.\n"
                    "Такого пользователя с такими данными не существует",
                )
                print("----------- DOESN'T USER INTO DB-----------")
                return redirect("accounts:login")  # Редирект при некорректном вводе

        print("-----------FORM DATA DOESN'T CORRECT-----------")
        print("-----------Отработали валидаторы django и кастомные-----------")
        return render(
            request=request,
            template_name=self.template_name,
            context={"form": form_login},
        )


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)  # Завершаем сессию пользователя
        return redirect("accounts:login")  # Перенаправляем на страницу логина
