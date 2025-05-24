from django.db import models


class Project(models.Model):
    # Base data
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    project_type = models.Choices(names=["feature", "series"], default="feature")
    description = models.CharField(max_length=500, blank=True)
    poster_path = models.CharField(max_length=200, blank=True)
    release_date = models.DateField(blank=True)
    adult = models.BooleanField(default=False)

    # Relationships
    cameras = models.ManyToManyField(
        "cameras.Camera",  # The name of the target table
        blank=True,
        related_name="used_in_projects",  # The backref name
    )

    formats = models.ManyToManyField(
        "cameras.Format",  # The name of the target table
        blank=True,
        related_name="used_in_projects",  # The backref name
    )

    # Data cache from TMDB
    tmdb_id = models.IntegerField(blank=True)
    tmdb_original_name = models.CharField(max_length=100, blank=True)
