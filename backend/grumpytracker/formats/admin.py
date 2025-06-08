from django.contrib import admin
from .models import Format, Source


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
