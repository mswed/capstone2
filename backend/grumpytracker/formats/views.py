from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from grumpytracker.utils import validate_required_fields, require_admin
import json
from loguru import logger

from .models import Format
from sources.models import Source
from cameras.models import Camera


@method_decorator(csrf_exempt, name="dispatch")
class FormatsListView(View):
    """
    Handle formats/ endpoint
    GET - Returns all of the formats in the DB
    POST - Creates a new format
    """

    def get(self, request) -> JsonResponse:
        """
        Return all existing formats
        """

        formats = Format.objects.all()
        data = []

        for fmt in formats:
            data.append(fmt.as_dict())

        return JsonResponse(data, safe=False)

    @method_decorator(require_admin)
    def post(self, request) -> JsonResponse:
        try:
            data = json.loads(request.body)

            # Validate our input
            error = validate_required_fields(
                data,
                [
                    "camera",
                    "source",
                    "image_format",
                    "sensor_width",
                    "sensor_height",
                    "image_width",
                    "image_height",
                ],
            )
            if error:
                return JsonResponse({"error": error}, status=400)

            logger.info("Passed validation")
            # We first need to find the camera and the source
            camera = get_object_or_404(Camera, id=data.get("camera"))
            source = get_object_or_404(Source, id=data.get("source"))

            fmt = Format.objects.create(
                camera=camera,
                source=source,
                image_format=data.get("image_format"),
                image_aspect=data.get("image_aspect", ""),
                format_name=data.get("format_name", ""),
                sensor_width=float(data.get("sensor_width")),
                sensor_height=float(data.get("sensor_height")),
                image_width=int(data.get("image_width")),
                image_height=int(data.get("image_height")),
                is_anamorphic=data.get("is_anamorphic", False),
                anamorphic_squeeze=data.get("anamorphic_squeeze", 1.0),
                is_desqueezed=data.get("is_desqueezed", False),
                pixel_aspect=float(data.get("pixel_aspect", 1.0)),
                is_downsampled=data.get("is_downsampled", False),
                is_upscaled=data.get("is_upscaled", False),
                codec=data.get("codec", ""),
                raw_recording_available=data.get("raw_recording_available", True),
                notes=data.get("notes", ""),
                make_notes=data.get("make_notes", ""),
            )

            if not fmt:
                return JsonResponse({"error": "Failed to create format"})

            return JsonResponse(
                {
                    "success": f"Created format {fmt.name}",
                    "format_id": fmt.id,
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class FormatDetailsView(View):
    """
    Handle formats/123 endpoint
    GET - Returns the full format's details
    PATH - Update a format
    DELETE - Delete a format
    """

    def get(self, request, format_id: int) -> JsonResponse:
        """
        Get a format by its interanl ID
        :param format_id: ID of format in the database
        """
        fmt = get_object_or_404(Format, id=format_id)
        return JsonResponse(fmt.as_dict(), safe=False)

    @method_decorator(require_admin)
    def patch(self, request, format_id):
        """
        Do a partial update on a format
        """

        # This is a simple temporary mapping, it the future it should
        # probably be switched to something like Pydantic
        field_types = {
            "sensor_width": float,
            "sensor_height": float,
            "anamorphic_squeeze": float,
            "pixel_aspect": float,
            "image_width": int,
            "image_height": int,
            "max_frame_rate": float,
            "is_anamorphic": bool,
            "is_desqueezed": bool,
            "is_downsampled": bool,
            "is_upscaled": bool,
            "raw_recording_available": bool,
        }

        fmt = get_object_or_404(Format, id=format_id)
        try:
            # Grab the project and the updated data
            data = json.loads(request.body)

            # Only update provided fields
            for field, value in data.items():
                if hasattr(fmt, field):
                    if field == "camera":
                        # We need to get the camera record for the update
                        camera = get_object_or_404(Camera, id=value)
                        value = camera
                    if field == "source":
                        # We need to get the source record for the update
                        source = get_object_or_404(Source, id=value)
                        value = source
                    elif field in field_types:
                        try:
                            if field_types[field] == "bool":
                                value = value.lower() == "true"
                            else:
                                value = field_types[field](value)
                        except (ValueError, TypeError):
                            return JsonResponse(
                                {"error": f"Invalid value for {field}: {value}"},
                                status=400,
                            )
                    setattr(fmt, field, value)

            fmt.save()
            return JsonResponse(
                {"success": f"Partialy updated format {fmt}", "format": fmt.as_dict()}
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @method_decorator(require_admin)
    def delete(self, request, format_id):
        """Handle DELETE /formats/123/"""
        fmt = get_object_or_404(Format, id=format_id)
        fmt.delete()
        return JsonResponse({"success": "Format deleted"})


class FormatsSearchView(View):
    """
    Handle formats/search endpoint
    GET - Returns the a list of formats based on a search query
    """

    def get(self, request) -> JsonResponse:
        """
        Search the database for a format based on model and sensor type
        """
        filter_map = {
            "make": "camera__make__name__icontains",
            "camera": "camera__model__icontains",
            "source": "source__name__icontains",
            "format": "format_search__icontains",
            "image_aspect": "image_aspect__icontains",
            "sensor_width": "sensor_width__icontains",
            "image_width": "image_width__icontains",
            "image_height": "image_height__icontains",
            "is_anamorphic": "bool",
            "anamorphic_squeeze": "anamorphic_squeeze__icontains",
            "is_desqueezed": "bool",
            "pixel_aspect": "pixel_aspect__icontains",
            "filmback_width_3de": "filmback_width_3de__icontains",
            "filmback_height_3de": "filmback_height_3de__icontains",
            "distortion_model_3de": "distortion_model_3de__icontains",
            "is_downsampled": "bool",
            "is_upscaled": "bool",
            "codec": "codec__icontains",
            "raw_recording_available": "bool",
            "notes": "notes__icontains",
            "make_notes": "make_notes__icontains",
            "tracking_workflow": "tracking_workflow__icontains",
        }

        filters = {}
        for param, lookup in filter_map.items():
            term = request.GET.get(param)
            if term:
                # We found the term in the query
                if lookup == "bool":
                    # We are looking for a boolean value
                    bool_value = term == "true"
                    filters[param] = bool_value

                else:
                    # We are looking for a regular value
                    filters[lookup] = term

        # Start building the query by getting all cameras with JOIN on makes
        formats = Format.objects.select_related("camera", "source")

        # Build the WHERE clause for each term
        if filters:
            formats = formats.filter(**filters)

        # Execute the query
        found_formats = [fmt.as_dict() for fmt in formats]

        return JsonResponse(found_formats, safe=False)
