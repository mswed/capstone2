import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from formats.models import Format
from cameras.models import Camera


@pytest.mark.django_db
class TestFormatModel:
    """
    Tests for the Format model
    """

    def test_format_simple_creation(self, single_make):
        """
        Test basic Camera creation without an image
        """
        camera = Camera.objects.create(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            sensor_size="Super 35",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
            notes="sample note",
            discontinued=True,
        )

        assert camera.make == single_make
        assert camera.model == "Alexa 35"
        assert (
            camera.sensor_type
            == "Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array"
        )
        assert camera.sensor_size == "Super 35"
        assert camera.max_filmback_width == 27.99
        assert camera.max_filmback_height == 19.22
        assert camera.max_image_width == 4608
        assert camera.max_image_height == 3164
        assert camera.min_frame_rate == 0.75
        assert camera.max_frame_rate == 120
        assert camera.notes == "sample note"
        assert camera.discontinued is True

        assert camera.created_at is not None
        assert camera.updated_at is not None

    def test_camera_optional_fields(self, single_make):
        """
        Some of our fields are optional see what happens if we skip them
        """
        camera = Camera.objects.create(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
        )
        assert camera.model == "Alexa 35"
        assert camera.sensor_size == "" or camera.sensor_size is None
        assert camera.notes == ""
        assert camera.discontinued is False

    def test_camera_with_image_creation(
        self, single_make, sample_image_file, temp_media_dir
    ):
        """
        Test Camera creation with logo from disk (local creation)
        """
        camera = Camera.create_with_image(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
            image_path=sample_image_file,
        )

        assert camera.model == "Alexa 35"
        assert camera.image is not None
        assert camera.image.name is not None
        assert "image_on_disk" in camera.image.name

        # Finally check that we actually created a file
        assert camera.image.file is not None

    def test_camera_with_missing_image_creation(self, single_make):
        """
        Test Camea creation where the provided logo does not exist on disk
        """
        camera = Camera.create_with_image(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
            image_path="no/such/path/image.png",
        )

        assert camera.model == "Alexa 35"
        assert not camera.image or camera.image is None

    def test_camera_with_uploaded_image_creation(
        self, single_make, sample_uploaded_file, temp_media_dir
    ):
        """
        Test Make creation with logo from upload (remote creation, mimics the final workflow)
        """
        camera = Camera.create_with_image(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
            image_file=sample_uploaded_file,
        )

        assert camera.model == "Alexa 35"
        assert camera.image is not None
        assert camera.image.name is not None
        assert "test_uploaded_image" in camera.image.name

    def test_update_image(self, single_make, sample_uploaded_file, temp_media_dir):
        """
        Can we update the image of a camera?
        """
        camera = Camera.objects.create(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
        )

        # Confirm that we created the Camera without a logo
        assert camera.model == "Alexa 35"
        assert not camera.image or camera.image is None

        # Update the logo
        camera.update_image(sample_uploaded_file)

        # Refresh the make with its data from the database
        camera.refresh_from_db()

        # Confirm that the logo has been updated
        assert camera.image is not None
        assert camera.image.name is not None
        assert "test_uploaded_image" in camera.image.name

    def test_update_and_replace_image(
        self, single_make, sample_uploaded_file, temp_media_dir
    ):
        """
        Can we update the logo of a Make if it already has a logo?
        """
        # Create an initial file
        initial_file = SimpleUploadedFile(
            name="initial_logo.png",
            content=b"fake image content",
            content_type="image/png",
        )
        camera = Camera.create_with_image(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
            image_file=initial_file,
        )

        initial_logo_name = camera.image.name

        # Update the logo
        camera.update_image(sample_uploaded_file)
        camera.refresh_from_db()

        # Confirm that the logo has been updated
        assert camera.image.name != initial_logo_name
        assert "test_uploaded_image" in camera.image.name

    def test_make_str(self, single_make):
        """
        The string representation of a make is its make and model
        """
        camera = Camera.objects.create(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
        )
        assert str(camera) == "Sample Make Alexa 35"

    def test_audit_fields(self, single_make):
        """
        We auto update audit fields on creation
        """
        camera = Camera.objects.create(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
        )

        assert camera.created_at is not None
        assert camera.updated_at is not None

        # Update the make
        original_updated_at = camera.updated_at
        camera.model = "Alexa 35 Updated"
        camera.save()

        assert camera.updated_at > original_updated_at

    def test_as_dict_without_logo(self, single_make):
        """
        Can we create a make without a logo?
        """
        camera = Camera.objects.create(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
        )

        result = camera.as_dict()

        expected_keys = {
            "id",
            "make",
            "make_name",
            "model",
            "sensor_type",
            "sensor_size",
            "max_filmback_width",
            "max_filmback_height",
            "max_image_width",
            "max_image_height",
            "min_frame_rate",
            "max_frame_rate",
            "notes",
            "discontinued",
            "image",
        }

        assert set(result.keys()) == expected_keys
        assert result["id"] == camera.id
        assert result["make"] == camera.make.id
        assert result["make_name"] == camera.make.name
        assert result["model"] == camera.model
        assert result["sensor_type"] == camera.sensor_type
        assert result["sensor_size"] == camera.sensor_size
        assert result["max_filmback_width"] == camera.max_filmback_width
        assert result["max_filmback_height"] == camera.max_filmback_height
        assert result["max_image_width"] == camera.max_image_width
        assert result["max_image_height"] == camera.max_image_height
        assert result["min_frame_rate"] == camera.min_frame_rate
        assert result["max_frame_rate"] == camera.max_frame_rate
        assert result["notes"] == camera.notes
        assert result["discontinued"] == camera.discontinued
        assert result["image"] is None

    def test_with_formats(self, single_make):
        """
        A camera should return formats that are attached to it (or an empty list in this case)
        """
        camera = Camera.objects.create(
            make=single_make,
            model="Alexa 35",
            sensor_type="Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            max_filmback_width=27.99,
            max_filmback_height=19.22,
            max_image_width=4608,
            max_image_height=3164,
            min_frame_rate=0.75,
            max_frame_rate=120,
        )

        result = camera.with_formats()

        expected_keys = {
            "id",
            "make",
            "make_name",
            "model",
            "sensor_type",
            "sensor_size",
            "max_filmback_width",
            "max_filmback_height",
            "max_image_width",
            "max_image_height",
            "min_frame_rate",
            "max_frame_rate",
            "notes",
            "discontinued",
            "image",
            "formats",
        }
        assert set(result.keys()) == expected_keys
        assert result["formats"] == []
