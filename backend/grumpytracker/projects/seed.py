from projects.models import Project
from django.db import transaction
from loguru import logger


@transaction.atomic
def clear_database():
    # Format.objects.delete() returns a tuple (count_deleted, dict_with_details)
    projects_deleted = Project.objects.all().delete()[0]

    logger.info(f"Deleted {projects_deleted} projects")

    return {
        "projects": projects_deleted,
    }


@transaction.atomic
def seed_projects():
    projects = [
        {
            "name": "Marvel's Daredevil",
            "url": "https://www.themoviedb.org/tv/61889-marvel-s-daredevil",
            "project_type": "series",
            "description": "Lawyer-by-day Matt Murdock uses his heightened senses from being blinded as a young boy to fight crime at night on the streets of Hell’s Kitchen as Daredevil.",
            "poster_path": "https://image.tmdb.org/t/p/w500/QWbPaDxiB6LW2LjASknzYBvjMj.jpg",
            "release_date": "2015-04-10",
            "tmdb_id": 61889,
        },
    ]

    created_projects = {}
    for p in projects:
        project, new = Project.objects.get_or_create(**p)
        created_projects[p["name"]] = project
        logger.info(f"{'Created' if new else 'Found'} project: {project.name}")

    return created_projects


def seed_db():
    projects = seed_projects()
