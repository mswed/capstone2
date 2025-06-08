from django.db import models


class Make(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def as_dict(self):
        return {"name": self.name, "website": self.website}
