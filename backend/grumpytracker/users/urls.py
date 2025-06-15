from django.urls import path
from . import views

urlpatterns = [
    path("auth", views.AuthView.as_view(), name="auth"),
    path("", views.UsersListView.as_view(), name="users"),
    path("<int:user_id>", views.UserDetailsView.as_view(), name="user"),
]
