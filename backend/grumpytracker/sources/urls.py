from django.urls import path
from . import views

urlpatterns = [
    path("", views.SourcesListView.as_view(), name="sources"),
    path("<int:source_id>", views.SourceDetailsView.as_view(), name="source"),
    path("search", views.SourcesSearchView.as_view(), name="search_sources"),
]
