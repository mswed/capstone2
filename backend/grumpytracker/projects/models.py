from django.db import models
from cameras.models import Camera
from formats.models import Format
from users.models import User


class Project(models.Model):
    PROJECT_TYPES = [("feature", "Feature"), ("episodic", "Episodic")]

    # Base data
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    project_type = models.CharField(
        max_length=10, choices=PROJECT_TYPES, default="feature"
    )
    description = models.CharField(max_length=500, blank=True)
    poster_path = models.CharField(max_length=200, blank=True)
    release_date = models.DateField(blank=True)
    adult = models.BooleanField(default=False)

    # Data cache from TMDB
    tmdb_id = models.IntegerField(blank=True, null=True)
    tmdb_original_name = models.CharField(max_length=100, blank=True)
    genres = models.JSONField(default=list, blank=True)
    rating = models.JSONField(default=list, blank=True)

    # Relationships
    cameras = models.ManyToManyField(
        "cameras.Camera",  # The name of the target table
        blank=True,
        related_name="used_in_projects",  # The backref name
    )

    formats = models.ManyToManyField(
        "formats.Format",  # The name of the target table
        through="ProjectFormat",
        blank=True,
        related_name="used_in_projects",  # The backref name
    )

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "project_type": self.project_type,
            "description": self.description,
            "poster_path": self.poster_path,
            "release_date": self.release_date,
            "adult": self.adult,
            "tmdb_id": self.tmdb_id,
            "tmdb_original_name": self.tmdb_original_name,
            "genres": self.genres,
            "rating": self.rating,
        }

    def with_formats(self):
        return {
            **self.as_dict(),
            "cameras": [cam.as_dict() for cam in self.cameras.all()],
            "formats": [fmt.as_dict() for fmt in self.formats.all()],
        }


class ProjectFormat(models.Model):
    """
    Projects have formats attached to them that users can up and down vote
    this sets up a through table for that
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    fmt = models.ForeignKey(Format, on_delete=models.CASCADE)

    # Audit fields
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["project", "fmt"]


class Vote(models.Model):
    """
    A model for a single format vote on a project
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    fmt = models.ForeignKey(Format, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    vote_type = models.CharField(choices=[("up", "upVote"), ("down", "downVote")])

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["project", "fmt", "user"]
