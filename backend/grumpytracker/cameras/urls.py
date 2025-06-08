from django.urls import path
from . import views

urlpatterns = [
    path("", views.CamerasListView.as_view(), name="cameras"),
    path("<int:camera_id>", views.CameraDetailsView.as_view(), name="camera"),
    path("search", views.CamerasSearchView.as_view(), name="search_cameras"),
]
