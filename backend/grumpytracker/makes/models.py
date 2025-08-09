from django.db import models
from django.core.files import File
import os


class Make(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="make_logos", blank=True, null=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    @classmethod
    def create_with_logo(cls, name, website, logo_file=None, logo_path=None):
        """
        Makes should have a logo, this function creates a record with a logo either
        form disk (for seeding) or from an API call (for the actual site)
        """

        make = cls.objects.create(name=name, website=website)

        if logo_path and os.path.exists(logo_path):
            # This is a local file used during seeding
            with open(logo_path, "rb") as f:
                make.logo.save(os.path.basename(logo_path), File(f), save=True)
        elif logo_file:
            # This is a file added via the API
            make.logo.save(logo_file.name, logo_file, save=True)

        return make

    def update_logo(self, logo_file):
        self.logo.save(logo_file.name, logo_file, save=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "website": self.website,
            "logo": self.logo.url if self.logo else None,
            "cameras_count": self.cameras.count(),
        }

    def with_cameras(self):
        return {
            **self.as_dict(),
            "cameras": [camera.as_dict() for camera in self.cameras.all()],
        }
