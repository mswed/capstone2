import requests
import json
from decouple import config
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Project
from .services import get_or_create_project_from_tmdb, refresh_project_from_tmdb
from cameras.models import Camera
from formats.models import Format

BASE_URL = "https://api.themoviedb.org/3"
TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w500"


# We need to disable csrf at the class level
@method_decorator(csrf_exempt, name="dispatch")
class ProjectsView(View):
    """
    Handle projects/ endpoint
    GET - Returns all of the projects in the DB
    POST - Creates a new project (or returns the id of an existing one)
    """

    def get(self, request):
        """
        Handle GET and return all existing projects
        """

        projects = Project.objects.all()
        data = []

        for project in projects:
            data.append({"id": project.id, "name": project.name, "url": project.url})

        return JsonResponse(data, safe=False)

    def post(self, request) -> JsonResponse:
        try:
            data = json.loads(request.body)
            tmdb_id = data.get("tmdb_id")
            project_type = data.get("project_type")

            if not tmdb_id:
                return JsonResponse({"error": "tmdb_id is required"}, status=400)

            project, created = get_or_create_project_from_tmdb(tmdb_id, project_type)
            if not project:
                # Something went wrong while trying to get the project
                return JsonResponse({"error": "Failed to get or create a project"})

            message = "Created new project" if created else "Project already exists"
            return JsonResponse(
                {"success": f"{message} {project.id}", "project_id": project.id}
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class ProjectDetailsView(View):
    """
    Handle projects/<int:project_id> endpoint
    GET - Returns the projects details
    PATCH - updates a project
    DELETE - Delete a project
    """

    def get(self, request, project_id):
        """
        Get a project by its interanl ID
        """
        project = get_object_or_404(Project, id=project_id)
        return JsonResponse(project.as_dict(), safe=False)

    def patch(self, request, project_id):
        """
        Do a partial update on a project
        """

        try:
            # Grab the project and the updated data
            project = get_object_or_404(Project, id=project_id)
            data = json.loads(request.body)

            # Update relationships
            if "format_ids" in data:
                # We are updating the formats
                # remove the formats from the base update
                format_ids = data.pop("format_ids")
                # Find the actual format objects
                formats = Format.objects.filter(id__in=format_ids)
                project.formats.set(formats)  # Update the project

            if "camera_ids" in data:
                # We are updating the cameras
                camera_ids = data.pop("camera_ids")
                cameras = Camera.objects.filter(id__in=camera_ids)
                project.cameras.set(cameras)  # Update the project

            # Only update provided fields
            for field, value in data.items():
                if hasattr(project, field):
                    setattr(project, field, value)

            project.save()
            return JsonResponse({"success": f"Partialy updated project {project.id}"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, project_id):
        """Handle DELETE /projects/123/"""
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return JsonResponse({"success": "Project deleted"})


def search(request):
    query = request.GET.get("q", "")
    if query:
        # Search local db first
        local_projects = Project.objects.filter(name__icontains=query)
        found_local_projects = []
        for project in local_projects:
            found_local_projects.append(
                {
                    "name": project.name,
                    "project_type": project.project_type,
                    "tmdb_id": project.tmdb_id,
                }
            )
        # Search TMDB second
        url = f"{BASE_URL}/search/multi?query={query}&include_adult=false&language=en-US&page=1"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {config('TMDB_API_READ_KEY')}",
        }

        response = requests.get(url, headers=headers)
        found_remote_projects = []
        results = response.json().get("results", None)
        if results:
            for project in results:
                if project.get("media_type") in ["movie", "tv"]:
                    found_remote_projects.append(
                        {
                            "name": project.get("title", project.get("name")),
                            "project_type": "episodic"
                            if project.get("media_type") == "tv"
                            else "feature",
                            "tmdb_id": project.get("id"),
                        }
                    )
        full_result = {
            "projects": {"local": found_local_projects, "remote": found_remote_projects}
        }
        return JsonResponse(full_result, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class ProjectsRestoreView(View):
    """
    Handle projects/restore endpoint for restoring projects to their TMDB state
    PATCH - Update a project to it matches its original TMDB data
    """

    def patch(self, request):
        """
        Restore multiple projects from TMDB
        """

        try:
            data = json.loads(request.body)
            project_ids = data.get("project_ids", [])

            results = []
            for pid in project_ids:
                try:
                    # Find the project based on its internal ID
                    project = get_object_or_404(Project, id=pid)

                    if project.tmdb_id:
                        # This project is attached to a TMDB record
                        updated_project = refresh_project_from_tmdb(project)
                        if updated_project:
                            results.append({"id": pid, "status": "restored"})
                        else:
                            results.append(
                                {
                                    "id": pid,
                                    "status": "error",
                                    "error": "Failed to update project",
                                }
                            )
                    else:
                        request.append(
                            {"id": pid, "status": "Not attached to TMDB project"}
                        )
                except Exception as e:
                    results.append({"id": pid, "status": "error", "error": str(e)})

            return JsonResponse({"results": results})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
