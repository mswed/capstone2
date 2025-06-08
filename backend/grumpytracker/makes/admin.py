from django.contrib import admin
from .models import Make


@admin.register(Make)
class MakesAdmin(admin.ModelAdmin):
    list_display = ["name", "website"]
    search_fields = ["name"]
