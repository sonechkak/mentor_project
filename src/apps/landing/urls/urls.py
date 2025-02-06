from django.urls import path

from landing.views import views

app_name = "landing"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
]
