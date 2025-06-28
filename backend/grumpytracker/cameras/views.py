from typing import List, Optional, Dict, Any
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from grumpytracker.utils import (
    validate_required_fields,
    login_required,
    require_owner_or_admin,
    require_admin,
)
import json
from loguru import logger

from cameras.models import Make, Camera


@method_decorator(csrf_exempt, name="dispatch")
class CamerasListView(View):
    """
    Handle cameras/manufacturers endpoint
    GET - Returns all of the cameras in the DB
    POST - Creates a new camera
    """

    def get(self, request) -> JsonResponse:
        """
        Return all existing cameras
        """

        cameras = Camera.objects.all()
        data = []

        for cam in cameras:
            data.append(cam.as_dict())

        return JsonResponse(data, safe=False)

    @method_decorator(require_admin)
    def post(self, request) -> JsonResponse:
        try:
            data = json.loads(request.body)

            # Validate our input
            error = validate_required_fields(
                data,
                [
                    "make",
                    "model",
                    "sensor_type",
                    "max_filmback_width",
                    "max_filmback_height",
                    "max_image_width",
                    "max_image_height",
                    "min_frame_rate",
                    "max_frame_rate",
                ],
            )
            if error:
                return JsonResponse({"error": error}, status=400)

            logger.info("Passed validation")
            # We first need to find the make
            make = get_object_or_404(Make, id=data.get("make"))

            camera = Camera.objects.create(
                make=make,
                model=data.get("model"),
                sensor_type=data.get("sensor_type"),
                max_filmback_width=data.get("max_filmback_width"),
                max_filmback_height=data.get("max_filmback_height"),
                max_image_width=data.get("max_image_width"),
                max_image_height=data.get("max_image_height"),
                min_frame_rate=data.get("min_frame_rate"),
                max_frame_rate=data.get("max_frame_rate"),
                notes=data.get("notes", ""),
                discontinued=data.get("discontinued", False),
            )

            if not camera:
                return JsonResponse({"error": "Failed to create camera"})

            return JsonResponse(
                {
                    "success": f"Created camera {camera.id}",
                    "camera_id": camera.id,
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class CameraDetailsView(View):
    """
    Handle cameras/123 endpoint
    GET - Returns the full camera's details
    PATH - Update a camera
    DELETE - Delete a camera
    """

    def get(self, request, camera_id: int) -> JsonResponse:
        """
        Get a camera by its interanl ID
        :param make_id: ID of camera in the database
        """
        camera = get_object_or_404(Camera, id=camera_id)
        return JsonResponse(camera.with_formats(), safe=False)

    @method_decorator(require_admin)
    def patch(self, request, camera_id):
        """
        Do a partial update on a camera
        """

        # Grab the project and the updated data
        camera = get_object_or_404(Camera, id=camera_id)

        try:
            data = json.loads(request.body)

            # Only update provided fields
            for field, value in data.items():
                if hasattr(camera, field):
                    if field == "make":
                        # We need to get the make record for the update
                        make = get_object_or_404(Make, id=value)
                        value = make
                    setattr(camera, field, value)

            camera.save()
            return JsonResponse({"success": f"Partialy updated camera {camera}"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @method_decorator(require_admin)
    def delete(self, request, camera_id):
        """Handle DELETE /cameras/123/"""
        camera = get_object_or_404(Camera, id=camera_id)
        camera.delete()
        return JsonResponse({"success": "Camera deleted"})


class CamerasSearchView(View):
    """
    Handle cameras/search endpoint
    GET - Returns the a list of cameras based on a search query
    """

    def get(self, request) -> JsonResponse:
        """
        Search the database for a camera based on make, model and sensor type
        """
        query = request.GET.get("q", "").strip()
        if not query:
            return JsonResponse({"error": "No query provided"})

        terms = query.split()

        # Start building the query by getting all cameras with JOIN on makes
        cameras = Camera.objects.select_related("make")

        # Build the WHERE clause for each term
        for term in terms:
            cameras = cameras.filter(
                Q(make__name__icontains=term)
                | Q(model__icontains=term)
                | Q(sensor_type__icontains=term)
            )

        # Execute the query
        found_cameras = [camera.as_dict() for camera in cameras]

        return JsonResponse(found_cameras, safe=False)
