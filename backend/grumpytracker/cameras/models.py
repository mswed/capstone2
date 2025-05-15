from django.db import models
from django.core.validators import MinValueValidator


class CameraManufacturer(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    def __str__(self):
        return str(self.name)


class Camera(models.Model):
    # Define the relationship
    manufacturer = models.ForeignKey(
        CameraManufacturer, on_delete=models.CASCADE, related_name="cameras"
    )

    # Camera info
    model = models.CharField(max_length=200)
    sensor_type = models.CharField(max_length=100)
    max_filmback_size = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Maximum filmback size in mm"
    )

    min_frame_rate = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    max_frame_rate = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.manufacturer.name} {self.model}"

    class Meta:
        unique_together = ["manufacturer", "model"]


class Format(models.Model):
    # Define the relationship
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="formats")

    # Format id
    image_format = models.CharField(max_length=5)
    image_aspect = models.CharField(max_length=10)
    format_name = models.CharField(max_length=100, blank=True)

    # Sensor data
    sensor_width = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    sensor_height = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )

    # Recording info
    image_width = models.IntegerField(validators=[MinValueValidator(0)])
    image_height = models.IntegerField(validators=[MinValueValidator(0)])
    is_downsampled = models.BooleanField(default=False)
    codec = models.CharField(max_length=20, blank=True)

    # Additional info
    anamorphic = models.BooleanField(default=False)
    pixel_aspect = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    notes = models.CharField(max_length=500)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        suffix = " (downsampled)" if self.is_downsampled else ""
        return f"{self.camera} {self.format_name}{suffix}"

    class Meta:
        unique_together = [
            "camera",
            "image_format",
            "image_aspect",
            "anamorphic",
            "codec",
        ]
