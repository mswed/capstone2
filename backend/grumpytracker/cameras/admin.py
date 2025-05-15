from django.contrib import admin
from .models import CameraManufacturer, Camera, Format


@admin.register(CameraManufacturer)
class CameraManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "website"]
    search_fields = ["name"]


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = [
        "manufacturer",
        "model",
        "sensor_type",
        "max_filmback_size",
        "min_frame_rate",
        "max_frame_rate",
    ]
    list_filter = ["manufacturer", "sensor_type"]
    search_fields = ["model", "manufacturer"]


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = [
        "camera",
        "image_format",
        "image_aspect",
        "format_name",
        "image_width",
        "image_height",
        "sensor_width",
        "sensor_height",
        "anamorphic",
        "pixel_aspect",
        "notes",
    ]
    list_filter = ["image_format", "anamorphic", "pixel_aspect"]
    search_fields = ["camera", "image_format", "image_aspect"]
