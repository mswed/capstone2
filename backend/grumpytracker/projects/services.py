import requests
from decouple import config
from .models import Project
from typing import Any, Dict, Optional, Tuple, List, TypedDict


BASE_URL = "https://api.themoviedb.org/3"
TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w500"


class NormalizedTMDBData(TypedDict):
    name: str
    project_type: str
    description: Optional[str]
    poster_path: Optional[str]
    release_date: Optional[str]
    tmdb_id: Optional[int]
    tmdb_original_name: Optional[str]
    adult: Optional[bool]
    genres: Optional[List[Dict[str, Any]]]
    rating: Optional[List[Dict[str, Any]]]


def get_or_create_project_from_tmdb(
    tmdb_id: int, project_type: str
) -> Tuple[Optional[Project], bool]:
    """
    Get an existing project from our DB or create a new one based on TMDB data
    :param tmdb_id: The id of the project on the TMDB API
    :param project_type: Episodic or Feature
    :returns: Project object and creation status
    """

    existing_project = Project.objects.filter(tmdb_id=tmdb_id).first()
    if existing_project:
        # We found the project in our database
        return (existing_project, False)

    tmdb_data = get_tmdb_project_data(tmdb_id, project_type)
    if not tmdb_data:
        # We did not find the project on TMDB
        return (None, False)

    # Normalize the data
    normalized = normalize_tmdb_data(tmdb_data, project_type)

    # We have a new project from TMDB create and return a cached version
    project = Project.objects.create(
        name=normalized.get("name"),
        project_type=normalized.get("project_type"),
        description=normalized.get("description"),
        poster_path=normalized.get("poster_path"),
        release_date=normalized.get("release_date"),
        adult=normalized.get("adult"),
        tmdb_id=normalized.get("tmdb_id"),
        tmdb_original_name=normalized.get("tmdb_original_name"),
        genres=normalized.get("genres"),
        rating=normalized.get("rating"),
    )

    return (project, True)


def refresh_project_from_tmdb(project: Project) -> Optional[Project]:
    """
    Overwrite the projects base data with info from TMDB

    :param project: Project object
    """

    tmdb_data = get_tmdb_project_data(project.tmdb_id, project.project_type)
    if tmdb_data:
        normalized = normalize_tmdb_data(tmdb_data, project.project_type)

        for field, value in normalized.items():
            setattr(project, field, value)

        project.save()

        return project

    return None


def get_tmdb_project_data(tmdb_id: int, project_type: str) -> Optional[Dict]:
    """
    Fetch data from TMDB based on an id and project type
    :param tmdb_id: The id of the project on the TMDB API
    :param project_type: Episodic or Feature
    :returns: JSON object with project data or None if nothing is found
    """

    if project_type == "episodic":
        url = f"{BASE_URL}/tv/{tmdb_id}?append_to_response=content_ratings"
    else:
        url = f"{BASE_URL}/movie/{tmdb_id}?append_to_response=release_dates"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {config('TMDB_API_READ_KEY')}",
    }

    response = requests.get(url, headers=headers)

    return response.json() if response.status_code == 200 else None


def process_rating(data: Dict) -> List[Dict[str, Any]]:
    """
    Process a projects rating and return it in a list of dicts containing region and rating
    :param data: Dictionary of project details from TMDB
    :returns: List of dictionaries with region and rating data
    """

    if "content_ratings" in data:
        # This is a TV show
        rating_data = data.get("content_ratings", {}).get("results", [])
        return [
            {"region": rd.get("iso_3166_1"), "rating": rd.get("rating")}
            for rd in rating_data
        ]
    else:
        rating_data = data.get("release_dates", {}).get("results")
        return [
            {
                "region": rd.get("iso_3166_1"),
                "rating": rd.get("release_dates")[0].get("certification"),
            }
            for rd in rating_data
        ]


def normalize_tmdb_data(data: Dict[str, Any], project_type: str) -> NormalizedTMDBData:
    """
    TMDB treates features and series differently this returns a mormalized version
    that has what our DB expects

    :param data: Dictionary containing raw data from TMDB
    :param project_type: Project type override
    :returns: Normalized dict
    """
    normalized: NormalizedTMDBData = {
        "name": data.get("name", data.get("title")),
        "project_type": project_type,
        "description": data.get("overview"),
        "poster_path": f"{TMDB_POSTER_BASE}{data.get('poster_path')}",
        "release_date": data.get("first_air_date", data.get("release_date")),
        "tmdb_id": data.get("id"),
        "adult": data.get("adult"),
        "tmdb_original_name": data.get("original_name", data.get("original_title")),
        "genres": [g["name"] for g in data.get("genres", [{}])],
        "rating": process_rating(data),
    }

    return normalized
