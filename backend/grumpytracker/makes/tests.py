import pytest
from django.test import override_settings
from makes.models import Make


@pytest.mark.django_db
class TestMakeModel:
    """
    Tests for the Make model
    """

    def test_make_simple_creation(self):
        """
        Test basic Make creation
        """
        make = Make.objects.create(name="Arri", website="https://www.arri.com")

        assert make.name == "Arri"
        assert make.website == "https://www.arri.com"
        assert not make.logo or make.logo is None
        assert make.created_at is not None
        assert make.updated_at is not None

    def test_make_website_is_optional(self):
        """
        Website should be optional
        """
        make = Make(name="RED")
        assert make.name == "RED"
        assert make.website == ""

    @override_settings(MEDIA_ROOT="/tmp/test_media")
    def test_make_with_logo_creation(self, sample_image_file, temp_media_dir):
        """
        Test Make creation with logo from disk (local creation)
        """
        make = Make.create_with_logo(
            name="Cannon", website="https://www.cannon.com", logo_path=sample_image_file
        )

        assert make.name == "Cannon"
        assert make.website == "https://www.cannon.com"
        assert make.logo is not None
        assert make.logo.name is not None
        assert "logo_on_disk" in make.logo.name

        # Finally check that we actually created a file
        assert make.logo.file is not None

    @override_settings(MEDIA_ROOT="/tmp/test_media")
    def test_make_with_missing_logo_creation(self):
        """
        Test Make creation where the provided logo does not exist on disk
        """
        make = Make.create_with_logo(
            name="Cannon",
            website="https://www.cannon.com",
            logo_path="no/such/path/image.png",
        )

        assert make.name == "Cannon"
        assert make.website == "https://www.cannon.com"
        assert not make.logo or make.logo is None

    @override_settings(MEDIA_ROOT="/tmp/test_media")
    def test_make_with_uploaded_logo_creation(
        self, sample_uploaded_file, temp_media_dir
    ):
        """
        Test Make creation with logo from upload (remote creation, mimics the final workflow)
        """
        make = Make.create_with_logo(
            name="Cannon",
            website="https://www.cannon.com",
            logo_file=sample_uploaded_file,
        )

        assert make.name == "Cannon"
        assert make.website == "https://www.cannon.com"
        assert make.logo is not None
        assert make.logo.name is not None
        assert "test_logo" in make.logo.name

    def test_update_logo(self, sample_uploaded_file, temp_media_dir):
        """
        Can we update the logo of a Make?
        """
        make = Make.objects.create(name="Arri", website="https://www.arri.com")

        # Confirm that we created the Make without a logo
        assert make.name == "Arri"
        assert make.website == "https://www.arri.com"
        assert not make.logo or make.logo is None

        # Update the logo
        make.update_logo(sample_uploaded_file)

        # Refresh the make with its data from the database
        make.refresh_from_db()

        # Confirm that the logo has been updated
        assert make.logo is not None
        assert make.logo.name is not None
        assert "test_logo" in make.logo.name

    def test_update_and_replace_logo(self, sample_uploaded_file, temp_media_dir):
        """
        Can we update the logo of a Make if it already has a logo?
        """
        # Create an initial file
        initial_file = SimpleUploadedFile(
            name="initial_logo.png",
            content=b"fake image content",
            content_type="image/png",
        )
        make = Make.create_with_logo(
            name="Arri", website="https://www.arri.com", logo_file=initial_file
        )

        initial_logo_name = make.logo.name

        # Update the logo
        make.update_logo(sample_uploaded_file)
        make.refresh_from_db()

        # Confirm that the logo has been updated
        assert make.logo.name != initial_logo_name
        assert "test_logo" in make.logo.name

    def test_make_str(self):
        """
        The string representation of a make is its name
        """
        make = Make(name="Sony")
        assert str(make) == "Sony"

    def test_audit_fields(self):
        """
        We auto update audit fields on creation
        """
        make = Make.objects.create(name="DJI", website="https://www.dji.com")

        assert make.created_at is not None
        assert make.updated_at is not None

        # Update the make
        original_updated_at = make.updated_at
        make.name = "DJI Updated"
        make.save()

        assert make.updated_at > original_updated_at

    def test_as_dict_without_logo(self):
        """
        Can we create a make without a logo?
        """
        make = Make.objects.create(
            name="Panasonic", website="https://www.panasonic.com"
        )
        result = make.as_dict()

        expected_keys = {"id", "name", "website", "logo", "cameras_count"}

        assert set(result.keys()) == expected_keys
        assert result["id"] == make.id
        assert result["name"] == make.name
        assert result["website"] == make.website
        assert result["logo"] is None
        assert result["cameras_count"] == 0

    def test_with_cameras(self):
        """
        A make should return cameras that are attached to it (or an empty list in this case)
        """
        make = Make.objects.create(name="Fujifilm", website="https://www.fujifilm.com")
        result = make.with_cameras()

        expected_keys = {"id", "name", "website", "logo", "cameras_count", "cameras"}
        assert set(result.keys()) == expected_keys
        assert result["cameras"] == []
