import requests
import json
from decouple import config
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Project, ProjectFormat
from .services import get_or_create_project_from_tmdb, refresh_project_from_tmdb
from grumpytracker.utils import (
    login_required,
    validate_required_fields,
    require_admin,
    require_owner_or_admin,
)
from cameras.models import Camera
from formats.models import Format

BASE_URL = "https://api.themoviedb.org/3"
TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w500"


# We need to disable csrf at the class level
@method_decorator(csrf_exempt, name="dispatch")
class ProjectsListView(View):
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

    @method_decorator(require_admin)
    def patch(self, request, project_id):
        """
        Do a partial update on a project
        """

        try:
            # Grab the project and the updated data
            project = get_object_or_404(Project, id=project_id)
            data = json.loads(request.body)

            # Only update provided fields
            for field, value in data.items():
                if hasattr(project, field):
                    setattr(project, field, value)

            project.save()
            return JsonResponse({"success": f"Partialy updated project {project.id}"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @method_decorator(require_owner_or_admin)
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


@method_decorator(csrf_exempt, name="dispatch")
class ProjectFormatsListView(View):
    """
    Handle projects/123/formats endpoint
    GET - Get all formats associated with the project
    POST - Add a format to the project
    """

    def get(self, request, project_id):
        """
        Handle GET and return all project's formats
        """

        # Grab the project
        project = get_object_or_404(Project, id=project_id)

        # Query the through table this will get us all of the formats and their votes total
        # We sort it by decending order
        project_formats = ProjectFormat.objects.filter(project=project).select_related(
            "fmt__camera__make"
        )
        data = []

        # Build a list of formats and their votes from our data
        for pfmt in project_formats:
            # Extract the format from the vote list
            format_info = pfmt.fmt.as_dict()
            format_info["added_by"] = pfmt.created_by.as_dict()
            data.append(format_info)

        return JsonResponse(data, safe=False)

    @method_decorator(login_required)
    def post(self, request, project_id) -> JsonResponse:
        """
        Add a format to the project
        """
        try:
            data = json.loads(request.body)
            validate_required_fields(data, ["format_id"])

            # Grab the project
            project = get_object_or_404(Project, id=project_id)
            fmt = get_object_or_404(Format, id=data.get("format_id"))

            try:
                project_format = ProjectFormat.objects.create(
                    project=project, fmt=fmt, created_by=request.user
                )
                if not project_format:
                    return JsonResponse({"error": "Failed to attach format"})
            except IntegrityError as e:
                return JsonResponse(
                    {"error": "Format already added to this project"}, status=400
                )

            return JsonResponse(
                {
                    "success": "Added format to project",
                    "project_format_id": project_format.id,
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class ProjectFormatDetailsView(View):
    """
    Handle projects/123/formats/456 endpoint
    PATCH - Upvote or downvote a format
    Delete - Remove a format
    """

    def patch(self, request, project_id, format__vote_id):
        """
        Handle GET and return all project's formats
        """

        # Grab the project
        format_vote = get_object_or_404(ProjectFormatVote, id=format__vote_id)

        try:
            data = json.loads(request.body)
            validate_required_fields(data, ["vote"])
            format_vote.votes += int(data.get("vote"))
            format_vote.save

            return JsonResponse({"success": "Updated vote count!"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def post(self, request, project_id) -> JsonResponse:
        """
        Add a format to the project
        """
        try:
            data = json.loads(request.body)
            validate_required_fields(data, ["format_id"])

            # Grab the project
            project = get_object_or_404(Project, id=project_id)
            fmt = get_object_or_404(Format, id=data.get("format_id"))

            try:
                format_vote = ProjectFormatVote.objects.create(project=project, fmt=fmt)
                if not format_vote:
                    return JsonResponse({"error": "Failed to attach format"})
            except IntegrityError as e:
                return JsonResponse(
                    {"error": "Format already added to this project"}, status=400
                )

            return JsonResponse(
                {"success": "Added format to project", "format_vote_id": format_vote.id}
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
