from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("<int:project_id>", views.by_id, name="project_by_id"),
]
