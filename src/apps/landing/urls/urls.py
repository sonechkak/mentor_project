from django.urls import path

from apps.landing.views import views

app_name = "landing"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),

    path('main-inf/save/text/', views.SaveMainInfTextView.as_view(), name='main_inf_save_text'), # изменения текста в maininf
    path('main-inf/save/img/', views.SaveMainInfImgView.as_view(), name='main_inf_save_img'), # изменение изображения в maininf
    path('main-inf/save/link/', views.SaveMainInfLinkView.as_view(), name='main_inf_save_link'), # изменение ссылок в maininf

    path('about_me/create/', views.AboutMeCreate.as_view(), name='about_me_create'), # создание нового блока aboutme
    path('about-me/edit/<int:pk>/', views.AboutMeUpdate.as_view(), name='about_me_edit'), # изменение блока aboutme
    path('about-me/delete/<int:pk>/', views.AboutMeDelete.as_view(), name='about_me_delete'), # удаление блока aboutme

    path('product/create/', views.ProductCreate.as_view(), name='product_create'),  # создание нового блока product
    path('product/edit/<int:pk>/', views.ProductUpdate.as_view(), name='product_edit'),  # изменение блока product
    path('product/delete/<int:pk>/', views.ProductDelete.as_view(), name='product_delete'),  # удаление блока product

    path('content/create/', views.ContentCreate.as_view(), name='content_create'),  # создание нового блока content
    path('content/edit/<int:pk>/', views.ContentUpdate.as_view(), name='content_edit'), # изменение блока content
    path('content/delete/<int:pk>/', views.ContentDelete.as_view(), name='content_delete'),  # удаление блока content





]
