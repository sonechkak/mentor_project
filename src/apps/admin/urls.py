from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("login/", views.AdminLoginView.as_view(), name="login"),
    path("logout/", views.AdminLogoutView.as_view(), name="logout"),
]
