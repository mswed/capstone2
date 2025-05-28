from typing import List, Optional, Dict, Any
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from grumpytracker.utils import validate_required_fields
import json

from cameras.models import Make


@method_decorator(csrf_exempt, name="dispatch")
class MakesView(View):
    """
    Handle cameras/manufacturers endpoint
    GET - Returns all of the manufacturers in the DB
    POST - Creates a new manufacturer
    """

    def get(self, request) -> JsonResponse:
        """
        Return all existing manufacturers
        """

        makes = Make.objects.all()
        data = []

        for make in makes:
            data.append({"id": make.id, "name": make.name})

        return JsonResponse(data, safe=False)

    def post(self, request) -> JsonResponse:
        try:
            data = json.loads(request.body)

            # Validate our input
            error = validate_required_fields(data, ["name", "website"])
            if error:
                return JsonResponse({"error": error}, status=400)

            make = Make.objects.create(
                name=data.get("name"), website=data.get("website")
            )
            if not make:
                return JsonResponse({"error": "Failed to create make"})

            return JsonResponse(
                {
                    "success": f"Created make {make.id}",
                    "manufacturer_id": make.id,
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class MakeDetailsView(View):
    """
    Handle cameras/makes/123 endpoint
    GET - Returns the full manufacturer's details (right now not different from the list)
    PATH - Update a manufacturer
    DELETE - Delete a manufacturer
    """

    def get(self, request, make_id: int) -> JsonResponse:
        """
        Get a manufacturer by its interanl ID
        :param make_id: ID of camera maker in the database
        """
        make = get_object_or_404(Make, id=make_id)
        return JsonResponse(make.as_dict(), safe=False)

    def patch(self, request, make_id):
        """
        Do a partial update on a make
        """

        try:
            # Grab the project and the updated data
            make = get_object_or_404(Make, id=make_id)
            data = json.loads(request.body)

            # Only update provided fields
            for field, value in data.items():
                if hasattr(make, field):
                    setattr(make, field, value)

            make.save()
            return JsonResponse({"success": f"Partialy updated make {make}"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, make_id):
        """Handle DELETE /cameras/makes/123/"""
        make = get_object_or_404(Make, id=make_id)
        make.delete()
        return JsonResponse({"success": "Make deleted"})
