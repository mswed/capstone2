from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http.multipartparser import MultiPartParser
from grumpytracker.utils import validate_required_fields, require_admin
import json
from loguru import logger

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
            data.append(make.as_dict())

        return JsonResponse(data, safe=False)

    @method_decorator(require_admin)
    def post(self, request) -> JsonResponse:
        try:
            # Because we are loading the logo we can not use
            # json we need to look at the POST data

            data = request.POST

            # Validate our input
            error = validate_required_fields(data, ["name", "website"])
            if error:
                return JsonResponse({"error": error}, status=400)

            make = Make.create_with_logo(
                name=data.get("name"),
                website=data.get("website"),
                logo_file=request.FILES.get("logo"),
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
        return JsonResponse(make.with_cameras(), safe=False)

    @method_decorator(require_admin)
    def patch(self, request, make_id):
        """
        Do a partial update on a make
        """

        # Django only deals automatically with multi part forms (which are needed for the images)
        # in POST requests so we need to manually parse the data

        if request.content_type.startswith("multipart/form-data"):
            parser = MultiPartParser(request.META, request, request.upload_handlers)
            data, files = parser.parse()

        else:
            data = json.loads(request.body)
            files = {}

        # Grab the make
        make = get_object_or_404(Make, id=make_id)

        try:
            # Only update provided fields
            for field, value in data.items():
                if hasattr(make, field):
                    setattr(make, field, value)

            make.save()

            # Update the logo
            if files.get("logo"):
                make.update_logo(files.get("logo"))

            return JsonResponse(
                {"success": f"Partialy updated make {make}", "make": make.as_dict()}
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @method_decorator(require_admin)
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
