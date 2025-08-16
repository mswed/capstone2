from logging import log
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from grumpytracker.utils import validate_required_fields, require_admin
import json
from loguru import logger

from .models import Source


@method_decorator(csrf_exempt, name="dispatch")
class SourcesListView(View):
    """
    Handle sources/ endpoint
    GET - Returns all of the sources in the DB
    POST - Creates a new source
    """

    def get(self, request) -> JsonResponse:
        """
        Return all existing sources
        """

        sources = Source.objects.all()
        data = []

        for source in sources:
            data.append(source.as_dict())

        return JsonResponse(data, safe=False)

    @method_decorator(require_admin)
    def post(self, request) -> JsonResponse:
        try:
            data = json.loads(request.body)

            # Validate our input
            error = validate_required_fields(
                data,
                [
                    "name",
                    "url",
                    "file_name",
                ],
            )
            if error:
                return JsonResponse({"error": error}, status=400)

            logger.info("Passed validation")

            source = Source.objects.create(
                name=data.get("name"),
                url=data.get("url"),
                file_name=data.get("file_name"),
                note=data.get("note"),
            )

            if not source:
                return JsonResponse({"error": "Failed to create source"})

            return JsonResponse(
                {
                    "success": f"Created source {source.name}",
                    "source": source.as_dict(),
                }
            )

        except Exception as e:
            logger.info(f"Something went wrong {e}")
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class SourceDetailsView(View):
    """
    Handle sources/123 endpoint
    GET - Returns the full source's details
    PATH - Update a source
    DELETE - Delete a source
    """

    def get(self, request, source_id: int) -> JsonResponse:
        """
        Get a format by its interanl ID
        :param source_id: ID of source in the database
        """
        source = get_object_or_404(Source, id=source_id)
        return JsonResponse(source.as_dict(), safe=False)

    @method_decorator(require_admin)
    def patch(self, request, source_id):
        """
        Do a partial update on a source
        """

        source = get_object_or_404(Source, id=source_id)
        try:
            # Grab the project and the updated data
            data = json.loads(request.body)

            # Only update provided fields
            for field, value in data.items():
                if hasattr(source, field):
                    setattr(source, field, value)

            source.save()
            return JsonResponse(
                {
                    "success": f"Partialy updated format {source}",
                    "source": source.as_dict(),
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @method_decorator(require_admin)
    def delete(self, request, source_id):
        """Handle DELETE /formats/123/"""
        source = get_object_or_404(Source, id=source_id)
        source.delete()
        return JsonResponse({"success": "Source deleted"})


class SourcesSearchView(View):
    """
    Handle sources/search endpoint
    GET - Returns the a list of sources based on a search query
    """

    def get(self, request) -> JsonResponse:
        """
        Search the database for a source based on name, url, filename and note
        """
        query = request.GET.get("q", "").strip()
        if not query:
            return JsonResponse({"error": "No query provided"})

        terms = query.split()

        # Start building the query by getting all cameras with JOIN on makes
        sources = Source.objects.all()

        # Build the WHERE clause for each term
        for term in terms:
            sources = sources.filter(
                Q(name__icontains=term)
                | Q(url__icontains=term)
                | Q(file_name__icontains=term)
                | Q(note__icontains=term)
            )

        # Execute the query
        found_sources = [source.as_dict() for source in sources]

        return JsonResponse(found_sources, safe=False)
