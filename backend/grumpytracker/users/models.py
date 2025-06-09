from typing import Dict, Any
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Extends the AbstractUser class, which already has username, email, first_name, last_name and password
    """

    role = models.CharField(max_length=100, blank=True, null=True)
    studio = models.CharField(max_length=100, blank=True, null=True)

    favorite_formats = models.ManyToManyField(
        "formats.Format",  # The name of the target table
        blank=True,
        related_name="favorited_by",  # The backref name
    )

    def __str__(self):
        return self.username

    def as_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "studio": self.studio,
            "fav_formats_ids": list(self.favorite_formats.values_list("id", flat=True)),
        }
