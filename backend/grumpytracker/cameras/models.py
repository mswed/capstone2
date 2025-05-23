from django.db import models
from django.core.validators import MinValueValidator


class CameraManufacturer(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        default=False, help_text="Was this model discontinued by the manufacturer?"
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.manufacturer.name} {self.model}"

    class Meta:
        unique_together = ["manufacturer", "model"]


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


class Format(models.Model):
    """
    Model for a recording format. This has all the information a tracker would be looking for.
    """

    # Define relationships
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="formats")
    source = models.ForeignKey(
        Source, on_delete=models.SET_NULL, null=True, blank=True, related_name="formats"
    )

    # Format id
    image_format = models.CharField(max_length=10)
    image_aspect = models.CharField(max_length=10, blank=True)
    format_name = models.CharField(max_length=100, blank=True)

    # Physical sensor info
    sensor_width = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    sensor_height = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )

    # Image resolution in pixels
    image_width = models.IntegerField(validators=[MinValueValidator(0)])
    image_height = models.IntegerField(validators=[MinValueValidator(0)])

    # Anamorphic information
    is_anamorphic = models.BooleanField(
        default=False, help_text="Is this format anamorphic?"
    )

    anamorphic_squeeze = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.0,
        help_text="Lens anamorphic factor (2.0 is the most common but can me 1.8, 1.33, etc)",
    )

    is_desqueezed = models.BooleanField(
        default=False, help_text="Has this footage already beed desqueezed in-camera?"
    )

    pixel_aspect = models.DecimalField(
        max_digits=4, decimal_places=2, default=1.0, help_text="Pixel aspect"
    )

    # 3DE information
    filmback_width_3de = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="3DE filmback width in mm",
    )
    filmback_height_3de = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="3DE filmback height in mm",
    )
    distortion_model_3de = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Recommended 3DE distortion for this format",
    )

    # Additionl info
    is_downsampled = models.BooleanField(default=False)
    is_upscaled = models.BooleanField(default=False)
    codec = models.CharField(max_length=20, blank=True)
    raw_recording_available = models.BooleanField(
        default=True,
        help_text="Is the raw, unprocessed format available for recording?",
    )

    # Different types of notes
    notes = models.CharField(max_length=500, blank=True, null=True)
    manufacturer_notes = models.CharField(max_length=500, blank=True, null=True)
    tracking_workflow = models.TextField(
        blank=True,
        null=True,
        help_text="Step-by-step instructions for setting up this format in tracking software",
    )

    display_name = f"{camera.model} {image_format} {image_aspect} {format_name} ({image_width} x {image_height} ) {'Anamorphic' if is_anamorphic else ''} {pixel_aspect if pixel_aspect != 1.0 else ''}"

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
            "format_name",
            "is_anamorphic",
            "codec",
            "is_downsampled",
            "pixel_aspect",
        ]

    def ensure_sperical_filmback(self) -> bool:
        """
        Ensure that the 3de filmaback is correct for a spherical lens while maintaining a pixel aspect of 1.0.
        If there's a mismatch between the filmback aspect and the image aspect adjust the filmback height to match
        """

        self.pixel_aspect = 1.0

        # Calculate aspect ratios
        sensor_aspect = float(self.sensor_width) / float(self.sensor_height)
        image_aspect = self.image_width / self.image_height

        if abs(sensor_aspect - image_aspect) > 0.001:
            # There is a mismatch between the two aspects adjust the filmback height
            self.filmback_width_3de = self.sensor_width
            self.filmback_height_3de = float(self.sensor_width) / image_aspect

            return True
        else:
            # There is no mismath we can use the sensor info
            self.filmback_width_3de = self.sensor_width
            self.filmback_height_3de = self.sensor_height

            return False

    def ensure_anamorphic_filmaback(self) -> bool:
        """
        Ensure that the 3de filmback is correct for an anamorphic lens
        :return: True if desqueezed False if not
        """
        # This is anamorphic footage figure out correct setup
        if not self.is_desqueezed:
            # This is raw footage
            if not self.filmback_width_3de or not self.filmback_height_3de:
                # Calculate correct filmback - simply multiply width by squeeze factor
                self.filmback_width_3de = self.sensor_width * self.anamorphic_squeeze
                self.filmback_height_3de = self.sensor_height
            return False
        else:
            # This is already desqueezed footage with PAR 1.0
            self.pixel_aspect = 1.0
            if not self.filmback_width_3de or not self.filmback_height_3de:
                # Calculate the filmback to represent the actual field of view

                # The desqueezed width should be the sensor's actual field of view
                desqueezed_width = self.sensor_width * self.anamorphic_squeeze

                # Calculate the aspect ratio change from sensor to final image
                original_aspect = self.sensor_width / self.sensor_height
                output_aspect = self.image_width / self.image_height

                # For 3.3K/4K example: (4096/1716) / (20.2/16.9) = 2.39/1.19 = 2.0
                aspect_change = output_aspect / original_aspect

                # Check if the aspect ratio changed substantially
                if abs(aspect_change - 1.0) > 0.1:
                    # Aspect ratio changed significantly (likely crop/reformat)
                    # Adjust the height to represent the portion of sensor actually used
                    self.filmback_width_3de = desqueezed_width
                    self.filmback_height_3de = desqueezed_width / output_aspect
                else:
                    # Simply use desqueezed dimensions
                    self.filmback_width_3de = desqueezed_width
                    self.filmback_height_3de = self.sensor_height

            return True

    def save(self, *args, **kwargs):
        """
        Overrides the model's save function. Used at the moment to update 3de values
        """
        if self.is_anamorphic:
            # This is an anamorphic format update the 3de filmabck
            desqueezed = self.ensure_anamorphic_filmaback()
            if desqueezed:
                self.distortion_model_3de = "Anamorphic Rescaled Degree 4"

                self.tracking_workflow = (
                    "IMPORTANT: Although this footage appears with square pixels (PAR 1.0), "
                    "it was shot in an anamorphic format and desqeezed in-camera!\n\n"
                    "1. Import with Pixel Aspect = 1.0\n"
                    "2. Set Filmback to {:.2f} x {:.2f} mm\n"
                    "3. Use '{}' lens distortion model\n"
                    "4. Set the distortion model's Anamorphic Squeeze to {:.1f}\n"
                    "5. Do NOT use Pixel Aspect for desqueezing"
                ).format(
                    self.filmback_width_3de or 0,
                    self.filmback_height_3de or 0,
                    self.distortion_model_3de,
                    self.anamorphic_squeeze,
                )
            else:
                self.distortion_model_3de = "Anamorphic Standard Degree 4"
        else:
            # This is a spherical format check if we had to update the 3de filmaback
            adjusted = self.ensure_sperical_filmback()
            if adjusted:
                self.tracking_workflow = (
                    "Note: The filmback height has been adjusted from the manufacturer's "
                    f"specification ({self.sensor_height} mm) to {self.filmback_height_3de:.2f} mm "
                    "to ensure a pixel aspect ratio of exactly 1.0 in 3DE.\n\n"
                    "This adjustment compensates for slight differences between the sensor's "
                    "physical aspect ratio and the recorded image aspect ratio."
                )
            self.distortion_model_3de = "Radial Standard Degree 4"

        # Run the parent class save function
        super().save(*args, **kwargs)

    def get_3de_setup_string(self) -> str:
        """Returns formatted string with complete 3DE setup values"""
        setup = (
            f"Format: {self.image_format} {self.image_aspect} ({self.format_name})\n"
        )
        setup += f"Resolution: {self.image_width} × {self.image_height}\n"
        setup += f"Pixel Aspect Ratio: {self.pixel_aspect_3de}\n"

        if self.filmback_width_3de and self.filmback_height_3de:
            setup += f"Filmback: {self.filmback_width_3de:.2f} mm × {self.filmback_height_3de:.2f} mm\n"

        if self.distortion_model_3de:
            setup += f"Recommended Distortion Model: {self.distortion_model_3de}\n"

        if self.is_anamorphic:
            setup += f"Anamorphic Squeeze Factor: {self.anamorphic_squeeze}\n"
            if self.is_desqueezed:
                setup += "IMPORTANT: This is desqueezed anamorphic footage!\n"

        return setup
