import pytest
from sources.models import Source


@pytest.mark.django_db
class TestSourceModel:
    """
    Tests for the Source model
    """

    def test_source_creation(self):
        """
        Test basic Camera creation without an image
        """
        source = Source.objects.create(
            name="Camera User Manual",
            url="https://www.source_url.com",
            file_name="camera_user_manual.pdf",
            note="This is not a real source!",
        )

        assert source.name == "Camera User Manual"
        assert source.url == "https://www.source_url.com"
        assert source.file_name == "camera_user_manual.pdf"
        assert source.note == "This is not a real source!"

    def test_source_optional_fields(self):
        """
        Some of our fields are optional see what happens if we skip them
        """
        source = Source.objects.create(
            name="Camera User Manual",
            url="https://www.source_url.com",
        )
        assert source.name == "Camera User Manual"
        assert source.file_name == ""
        assert source.note is None

    def test_source_str(self):
        """
        The string representation of a source is its name
        """
        source = Source.objects.create(
            name="Camera User Manual",
            url="https://www.source_url.com",
            file_name="camera_user_manual.pdf",
            note="This is not a real source!",
        )

        assert str(source) == "Camera User Manual"

    def test_audit_fields(self, single_make):
        """
        We auto update audit fields on creation
        """
        source = Source.objects.create(
            name="Camera User Manual",
            url="https://www.source_url.com",
            file_name="camera_user_manual.pdf",
            note="This is not a real source!",
        )

        assert source.created_at is not None
        assert source.updated_at is not None

        # Update the make
        original_updated_at = source.updated_at
        source.name = "Camera User Manual Updated"
        source.save()

        assert source.updated_at > original_updated_at

    def test_as_dict(self):
        """
        Can we get a serialized version of the model?
        """
        source = Source.objects.create(
            name="Camera User Manual",
            url="https://www.source_url.com",
            file_name="camera_user_manual.pdf",
            note="This is not a real source!",
        )

        result = source.as_dict()

        expected_keys = {
            "id",
            "name",
            "url",
            "file_name",
            "note",
        }

        assert set(result.keys()) == expected_keys
        assert result["id"] == source.id
        assert result["name"] == source.name
        assert result["url"] == source.url
        assert result["file_name"] == source.file_name
        assert result["note"] == source.note
