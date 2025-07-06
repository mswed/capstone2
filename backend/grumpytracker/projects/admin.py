from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "url"]
    search_fields = ["name"]

    fieldsets = (("Project Info", {"fields": ("name", "url")}),)
