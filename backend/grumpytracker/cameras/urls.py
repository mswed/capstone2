from django.urls import path
from . import views

urlpatterns = [
    path("makes/", views.MakesView.as_view(), name="makes"),
    path("makes/<int:make_id>", views.MakeDetailsView.as_view(), name="make"),
    # path("<int:project_id>", views.ProjectDetailsView.as_view(), name="project"),
    # path("search/", views.search, name="search_projects"),
    # path("restore/", views.ProjectsRestoreView.as_view(), name="restore_projects"),
]
