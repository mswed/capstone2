from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from grumpytracker.utils import validate_required_fields
import json

from .models import Make


@method_decorator(csrf_exempt, name="dispatch")
class MakesListView(View):
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
                    "make_id": make.id,
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

        # Grab the project and the updated data
        make = get_object_or_404(Make, id=make_id)

        try:
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


class MakesSearchView(View):
    """
    Handle cameras/makes/search endpoint
    GET - Returns the a list of makes based on a search query
    """

    def get(self, request) -> JsonResponse:
        """
        Search the database for a make based on its name
        """
        query = request.GET.get("q", "")
        if query:
            makes = Make.objects.filter(name__icontains=query)
            found_makes = []
            for make in makes:
                found_makes.append(
                    {
                        "name": make.name,
                        "website": make.website,
                        "id": make.id,
                    }
                )

            return JsonResponse(found_makes, safe=False)

        return JsonResponse({"error": "No query provided"})
