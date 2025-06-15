from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProjectsListView.as_view(), name="projects"),
    path("<int:project_id>", views.ProjectDetailsView.as_view(), name="project"),
    path("search/", views.search, name="search_projects"),
    path("restore/", views.ProjectsRestoreView.as_view(), name="restore_projects"),
    path(
        "<int:project_id>/formats/",
        views.ProjectFormatsListView.as_view(),
        name="format_votes",
    ),
    path(
        "<int:project_id>/formats/<int:format_id>",
        views.ProjectFormatDetailsView.as_view(),
        name="format_vote",
    ),
]
