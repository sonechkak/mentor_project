from django.urls import path

from apps.landing.views import views

app_name = "landing"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("aboutme/create", views.AboutMeCreate.as_view(), name="about-me-create"),
    # URL для сохранения текста
    path('save_main_inf_text/', views.SaveMainInfTextView.as_view(), name='save_main_inf_text'),

    # URL для сохранения изображения
    path('save_main_inf_img/', views.SaveMainInfImgView.as_view(), name='save_main_inf_img'),
    #path('save_main_inf/', views.save_main_inf, name='save-main-inf'),
]
