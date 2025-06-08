from django.urls import path
from . import views

urlpatterns = [
    path("", views.FormatsListView.as_view(), name="formats"),
    path("<int:format_id>", views.FormatDetailsView.as_view(), name="format"),
    path("search", views.FormatsSearchView.as_view(), name="search_formats"),
]
