from django.urls import path

from apps.admin.views import api_views

urlpatterns = [
    path("generate-password/", api_views.GeneratePasswordView.as_view(), name="generate-password"),
    path("blog/article/<slug:skug>/delete/", api_views.ArticleDeleteView.as_view(), name="article-delete-by-slug"),
    path("blog/category/<int:category_id>/delete/", api_views.CategoryDeleteView.as_view(),
         name="category-delete-by-id"),
]
