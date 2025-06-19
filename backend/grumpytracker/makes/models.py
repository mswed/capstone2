from django.db import models


class Make(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="make_logos", blank=True, null=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "website": self.website,
            "logo": self.logo.url if self.logo else None,
        }

    def with_cameras(self):
        return {
            **self.as_dict(),
            "cameras": [camera.as_dict() for camera in self.cameras.all()],
        }
