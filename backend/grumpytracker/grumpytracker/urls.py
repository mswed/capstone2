"""
URL configuration for grumpytracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import StatsView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/makes/", include("makes.urls")),
    path("api/v1/cameras/", include("cameras.urls")),
    path("api/v1/formats/", include("formats.urls")),
    path("api/v1/sources/", include("sources.urls")),
    path("api/v1/projects/", include("projects.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/stats/", StatsView.as_view(), name="stats"),
]

if settings.DEBUG:
    # When in development mode Django loads the images
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
