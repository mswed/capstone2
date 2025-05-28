from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProjectsView.as_view(), name="projects"),
    path("<int:project_id>", views.ProjectDetailsView.as_view(), name="project"),
    path("search/", views.search, name="search_projects"),
    path("restore/", views.ProjectsRestoreView.as_view(), name="restore_projects"),
]
