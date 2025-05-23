from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Extends the AbstractUser class, which already has username, email, first_name, last_name and password
    """

    role = models.CharField(max_length=100, blank=True)
    studio = models.CharField(max_length=100, blank=True)

    favorite_formats = models.ManyToManyField(
        "cameras.Format",  # The name of the target table
        blank=True,
        related_name="favorited_by",  # The backref name
    )

    def __str__(self):
        return self.username
