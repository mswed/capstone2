from django.urls import path
from . import views

urlpatterns = [
    path("", views.CamerasView.as_view(), name="cameras"),
    path("<int:camera_id>", views.CameraDetailsView.as_view(), name="camera"),
    path("search", views.CameraSearchView.as_view(), name="search_cameras"),
    path("makes/", views.MakesView.as_view(), name="makes"),
    path("makes/<int:make_id>", views.MakeDetailsView.as_view(), name="make"),
    path("makes/search", views.MakeSearchView.as_view(), name="search_makes"),
    # path("search/", views.search, name="search_projects"),
    # path("restore/", views.ProjectsRestoreView.as_view(), name="restore_projects"),
]
