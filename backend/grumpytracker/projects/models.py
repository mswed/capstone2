from django.db import models
from formats.models import Format
from users.models import User


class Project(models.Model):
    PROJECT_TYPES = [("feature", "Feature"), ("episodic", "Episodic")]

    # Base data
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    project_type = models.CharField(
        max_length=10, choices=PROJECT_TYPES, default="feature"
    )
    description = models.CharField(max_length=500, blank=True, null=True)
    poster_path = models.CharField(max_length=200, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    adult = models.BooleanField(default=False)

    # Data cache from TMDB
    tmdb_id = models.IntegerField(blank=True, null=True)
    tmdb_original_name = models.CharField(max_length=100, blank=True, null=True)
    genres = models.JSONField(default=list, blank=True, null=True)
    rating = models.JSONField(default=list, blank=True, null=True)

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

    def with_formats(self, user=None):
        """
        Returns the project with its cameras and formats AND the votes on each format
        """
        formats_with_votes = []

        for fmt in self.formats.all():
            # Get vote counts for each format
            votes = Vote.objects.filter(project=self, fmt=fmt)
            up_votes = votes.filter(vote_type="up").count()
            down_votes = votes.filter(vote_type="down").count()

            # If we have a user check how they voted
            user_vote = None
            if user is not None:
                try:
                    user_vote_obj = Vote.objects.get(project=self, fmt=fmt, user=user)
                    user_vote = user_vote_obj.vote_type
                except Vote.DoesNotExist:
                    user_vote = None
            format_data = {
                **fmt.as_dict(),
                "up_votes": up_votes,
                "down_votes": down_votes,
                "total_votes": up_votes + down_votes,
                "score": up_votes - down_votes,
                "user_vote": user_vote,
            }

            formats_with_votes.append(format_data)

        return {
            **self.as_dict(),
            "cameras": [cam.as_dict() for cam in self.cameras.all()],
            "formats": formats_with_votes,
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

    def __str__(self):
        # TODO: This was set up like __repr__ which is technically wrong
        return f"<Vote Project: {self.project} Format: {self.fmt} User: {self.user} Vote: {self.vote_type}>"
