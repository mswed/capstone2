from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Project


def project_list(request):
    projects = Project.objects.all()
    data = []

    for project in projects:
        data.append({"id": project.id, "name": project.name, "url": project.url})

    return JsonResponse(data, safe=False)


def by_id(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    data = {"project": {"id": project.id, "name": project.name, "url": project.url}}
    return JsonResponse(data, safe=False)
