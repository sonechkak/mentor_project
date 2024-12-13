from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import AdminLoginForm
from .utils import normalize_email



class AdminLoginView(View):
    template_name = 'admin/admin_login.html'

    def get(self, request):
        admin_login_form = AdminLoginForm()
        return render(request, self.template_name, {'form': admin_login_form})

    def post(self, request):
        admin_login_form = AdminLoginForm(request.POST)
        if admin_login_form.is_valid():
            email = admin_login_form.cleaned_data['email']
            password = admin_login_form.cleaned_data['password']

            email = normalize_email(email)
            # Аутентификация пользователя
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active and not user.is_admin:
                    # Проверка на активность и что пользователь не администратор
                    print("-----------DO NOT ADMIN-----------")
                    messages.error(request, "Вы не являетесь администратором")
                    return redirect('admin:login')  # Редирект для неадминистратора

                if user.is_active and user.is_admin:
                    # Проверка на активность и что пользователь явл. администратор
                    print("-----------ADMIN-----------")
                    login(request, user)
                    messages.success(request, "Вы успешно вошли в систему.")
                    return redirect('admin:login')  # Редирект для успешного входа
            else:
                messages.error(request, "Такого пользователя с такими данными не существует")
                print("----------- DOESN'T USER INTO DB-----------")
                return redirect('admin:login')  # Редирект при некорректном вводе

        print("-----------FORM DATA DOESN'T CORRECT-----------")
        print("-----------Отработали валидаторы django и кастомные-----------")
        return render(request, self.template_name, {'form': admin_login_form})


class AdminLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)  # Завершаем сессию пользователя
        return redirect("admin:login")  # Перенаправляем на страницу логина
