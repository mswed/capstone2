from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Extends the AbstractUser class, which already has username, email, first_name, last_name and password
    """

    role = models.CharField(max_length=100, blank=True)
    studio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username
