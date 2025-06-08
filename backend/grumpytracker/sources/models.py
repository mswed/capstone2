from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    file_name = models.CharField(max_length=100, blank=True)
    note = models.CharField(max_length=500, blank=True, null=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
