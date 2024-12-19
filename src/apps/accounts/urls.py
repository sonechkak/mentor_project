from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
