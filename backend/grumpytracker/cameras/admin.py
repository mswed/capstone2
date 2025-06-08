from django.contrib import admin
from .models import Camera


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = [
        "make",
        "model",
        "sensor_type",
        "max_filmback_width",
        "max_filmback_height",
        "max_image_width",
        "max_image_height",
        "min_frame_rate",
        "max_frame_rate",
    ]
    list_filter = ["make", "sensor_type"]
    search_fields = ["model", "make"]
