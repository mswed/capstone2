from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from projects.models import Project
from makes.models import Make
from cameras.models import Camera
from formats.models import Format


@method_decorator(csrf_exempt, name="dispatch")
class StatsView(View):
    """
    Handle stats/ endpoint
    GET - Returns count of items in database
    """

    def get(self, request) -> JsonResponse:
        """
        Return counts
        """

        makes = Make.objects.count()
        cameras = Camera.objects.count()
        formats = Format.objects.count()
        projects = Project.objects.count()

        return JsonResponse(
            {
                "makes": makes,
                "cameras": cameras,
                "formats": formats,
                "projects": projects,
            },
            safe=False,
        )
