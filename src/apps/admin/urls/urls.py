from django.urls import path

from apps.admin.views import views

app_name = "admin"

urlpatterns = [
    path("list-users/", views.ListUsersView.as_view(), name="list_users"),
    path("edit/user/<int:id>/", views.EditUserView.as_view(), name="edit-user"),
    path("create/user/", views.CreateUserView.as_view(), name="create-user"),

    path("category-list/", views.CategoryListView.as_view(), name="category-list"),
    path("category/create/", views.CategoryCreateView.as_view(), name="category-create"),
    path("category/edit/<slug:cat_slug>/", views.CategoryEditView.as_view(), name="category-edit"),

    path("list-tags/", views.TagListView.as_view(), name="list_tags"),
    path("edit/tag/<slug:slug>/", views.TagEditView.as_view(), name="edit-tag"),
    path("create/tag/", views.TagCreateView.as_view(), name="create-tag"),
    path('tag/delete/<slug:slug>/', views.TagDeleteView.as_view(), name="delete-tag"),
]
