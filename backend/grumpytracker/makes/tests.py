import pytest
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from makes.models import Make


@pytest.mark.django_db
class TestMakeModel:
    """
    Tests for the Make model
    """

    def test_make_creation(self):
        """
        Test basic Make creation
        """
        make = Make.objects.create(name="Arri", website="https://www.arri.com")

        assert make.name == "Arri"
        assert make.website == "https://www.arri.com"
        assert not make.logo or make.logo is None
        assert make.created_at is not None
        assert make.updated_at is not None

    def test_make_str(self):
        make = Make(name="Sony")
        assert str(make) == "Sony"

    def test_make_website_is_optional(self):
        make = Make(name="RED")
        assert make.name == "RED"
        assert make.website == ""

    def test_audit_fields(self):
        make = Make.objects.create(name="DJI", website="https://www.dji.com")

        assert make.created_at is not None
        assert make.updated_at is not None

        # Update the make
        original_updated_at = make.updated_at
        make.name = "DJI Updated"
        make.save()

        assert make.updated_at > original_updated_at

    def test_as_dict_without_logo(self):
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
        make = Make.objects.create(name="Fujifilm", website="https://www.fujifilm.com")
        result = make.with_cameras()

        expected_keys = {"id", "name", "website", "logo", "cameras_count", "cameras"}
        assert set(result.keys()) == expected_keys
        assert result["cameras"] == []
