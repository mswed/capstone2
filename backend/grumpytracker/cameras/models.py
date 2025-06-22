from django.db import models
from django.core.validators import MinValueValidator
from makes.models import Make
from typing import Dict, Any


class Camera(models.Model):
    # Define the relationship
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name="cameras")

    # Camera info
    model = models.CharField(max_length=200)
    sensor_type = models.CharField(max_length=100)
    sensor_size = models.CharField(max_length=100, blank=True, null=True)
    max_filmback_width = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        help_text="Maximum filmback size in mm",
    )
    max_filmback_height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        help_text="Maximum filmback size in mm",
    )

    max_image_width = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    max_image_height = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    min_frame_rate = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    max_frame_rate = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )

    notes = models.CharField(max_length=500, blank=True)
    discontinued = models.BooleanField(
        default=False, help_text="Was this model discontinued by the make?"
    )

    image = models.ImageField(upload_to="camera_images/", blank=True, null=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.make.name} {self.model}"

    def as_dict(self) -> Dict[str, Any]:
        """
        Return the model as a dictionary
        """

        return {
            "id": self.id,
            "make": self.make.id,
            "make_name": self.make.name,
            "model": self.model,
            "sensor_type": self.sensor_type,
            "sensor_size": self.sensor_size,
            "max_filmback_width": self.max_filmback_width,
            "max_filmback_height": self.max_filmback_height,
            "max_image_width": self.max_image_width,
            "max_image_height": self.max_image_height,
            "min_frame_rate": self.min_frame_rate,
            "max_frame_rate": self.max_frame_rate,
            "notes": self.notes,
            "discontinued": self.discontinued,
            "image": self.image.url if self.image else None,
        }

    def with_formats(self):
        return {
            **self.as_dict(),
            "formats": [fmt.as_dict() for fmt in self.formats.all()],
        }

    class Meta:
        unique_together = ["make", "model"]
