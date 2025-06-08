from django.urls import path
from . import views

urlpatterns = [
    path("", views.MakesListView.as_view(), name="makes"),
    path("<int:make_id>", views.MakeDetailsView.as_view(), name="make"),
    path("search", views.MakesSearchView.as_view(), name="search_makes"),
]
