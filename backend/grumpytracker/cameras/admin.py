from django.contrib import admin
from .models import CameraManufacturer, Camera, Format, Source


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
        "max_filmback_width",
        "max_filmback_height",
        "max_image_width",
        "max_image_height",
        "min_frame_rate",
        "max_frame_rate",
    ]
    list_filter = ["manufacturer", "sensor_type"]
    search_fields = ["model", "manufacturer"]


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = [
        "camera",
        "source",
        "image_format",
        "image_aspect",
        "format_name",
        "image_width",
        "image_height",
        "sensor_width",
        "sensor_height",
        "is_anamorphic",
        "anamorphic_squeeze",
        "is_desqueezed",
        "pixel_aspect",
        "filmback_width_3de",
        "filmback_height_3de",
        "distortion_model_3de",
        "is_downsampled",
        "codec",
        "notes",
        "tracking_workflow",
    ]
    list_filter = ["image_format", "is_anamorphic", "pixel_aspect"]
    search_fields = ["camera", "image_format", "image_aspect"]


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "url",
        "note",
    ]
    list_filter = ["name", "url"]
    search_fields = ["name", "url"]
