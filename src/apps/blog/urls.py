from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("<slug:slug>/", views.ArticleDetail.as_view(), name="article_detail"),
    path("", views.ArticleListView.as_view(), name="article_list"),
    path("tag/<slug:slug>/", views.ArticleByTag.as_view(), name="articles_by_tag"),
]
