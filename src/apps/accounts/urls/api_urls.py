from django.urls import path

from apps.accounts.views import api_views

urlpatterns = [
    path("users/", api_views.UserListCreateView.as_view(), name="user-create-and-list"),
    path('users/<int:pk>/', api_views.UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path("users/<int:id>/change-password/",
         api_views.UserChangePasswordView.as_view(),
         name="change-password",
         ),
]
