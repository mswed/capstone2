from django.db import models


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
            "camera_ids": list(self.cameras.values_list("id", flat=True)),
            "format_ids": list(self.formats.values_list("id", flat=True)),
        }
