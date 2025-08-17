from pprint import pprint
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.client import encode_multipart, BOUNDARY
from formats.models import Format

User = get_user_model()


class TestFormatsListView:
    """
    Tests for the Formats list view
    """

    @pytest.mark.django_db
    def test_get_all_formats_empty(self, client):
        """
        Test getting all formats when we don't have any records in the DB
        """

        res = client.get(reverse("formats"))

        assert res.status_code == 200
        data = res.json()
        assert data == []

    @pytest.mark.django_db
    def test_get_all_formats_with_data(self, client, multiple_formats):
        """
        Test getting all formats when we have records in the DB
        """

        res = client.get(reverse("formats"))

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 4

        # Check the names
        formats = [fmt["image_format"] for fmt in data]
        assert "4.6K" in formats
        assert "3K" in formats
        assert "4K" in formats
        assert "2K" in formats

        for format_data in data:
            expected_keys = {
                "id",
                "camera",
                "camera_model",
                "make_name",
                "source",
                "image_format",
                "image_aspect",
                "format_name",
                "sensor_width",
                "sensor_height",
                "image_width",
                "image_height",
                "pixel_aspect",
                "is_anamorphic",
                "is_desqueezed",
                "anamorphic_squeeze",
                "filmback_width_3de",
                "filmback_height_3de",
                "distortion_model_3de",
                "is_downsampled",
                "is_upscaled",
                "codec",
                "raw_recording_available",
                "notes",
                "make_notes",
                "tracking_workflow",
            }
            assert set(format_data.keys()) == expected_keys

    @pytest.mark.django_db
    def test_create_format(self, admin_client, single_camera, single_source):
        """
        Can we create a format?
        """
        data = {
            "camera": single_camera.id,
            "image_format": "6K",
            "image_aspect": "2:1",
            "sensor_width": 27.03,
            "sensor_height": 13.52,
            "image_width": 6144,
            "image_height": 3072,
            "codec": "R3D",
            "source": single_source.id,
        }

        res = admin_client.post(
            reverse("formats"), data, content_type="application/json"
        )

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data
        assert "format_id" in res_data

        # Check the database to make sure the record was created
        fmt = Format.objects.get(id=res_data["format_id"])
        assert fmt.image_format == "6K"
        assert fmt.image_aspect == "2:1"
        assert fmt.sensor_width == 27.03

    @pytest.mark.django_db
    def test_create_format_with_missing_fields(self, admin_client):
        """
        Missing required fields should return an error
        """
        # TODO: Test multiple missing fields this only checks for camera
        data = {
            "image_format": "Incomplete Format",
        }
        res = admin_client.post(
            reverse("formats"), data, content_type="application/json"
        )

        assert res.status_code == 400
        res_data = res.json()
        assert "error" in res_data
        assert "camera is required" in res_data["error"]

    @pytest.mark.django_db
    def test_create_format_not_authenticated(
        self, client, single_camera, single_source
    ):
        """
        If we did not log in we can not create a format
        """
        data = {
            "camera": single_camera.id,
            "image_format": "6K",
            "image_aspect": "2:1",
            "sensor_width": 27.03,
            "sensor_height": 13.52,
            "image_width": 6144,
            "image_height": 3072,
            "codec": "R3D",
            "source": single_source.id,
        }

        res = client.post(reverse("formats"), data, content_type="application/json")

        assert res.status_code == 401
        res_data = res.json()
        assert res_data["error"] == "Login required"

    @pytest.mark.django_db
    def test_create_format_not_admin(
        self, regular_user, client, single_camera, single_source
    ):
        """
        Regular users are not allowed to create Makes
        """

        # We can use our regular user fixture to log in
        client.force_login(regular_user)

        data = {
            "camera": single_camera.id,
            "image_format": "6K",
            "image_aspect": "2:1",
            "sensor_width": 27.03,
            "sensor_height": 13.52,
            "image_width": 6144,
            "image_height": 3072,
            "codec": "R3D",
            "source": single_source.id,
        }

        res = client.post(reverse("formats"), data, content_type="application/json")

        assert res.status_code == 403
        res_data = res.json()
        assert res_data["error"] == "Permission denied!"


class TestFormatDetailsView:
    """
        Tests for the Format details view
    db"""

    @pytest.mark.django_db
    def test_get_format_details(self, single_format, client):
        """
        Test that we can get a format's details
        """
        res = client.get(reverse("format", args=[single_format.id]))

        assert res.status_code == 200

        data = res.json()
        expected_keys = {
            "id",
            "camera",
            "camera_model",
            "make_name",
            "source",
            "image_format",
            "image_aspect",
            "format_name",
            "sensor_width",
            "sensor_height",
            "image_width",
            "image_height",
            "pixel_aspect",
            "is_anamorphic",
            "is_desqueezed",
            "anamorphic_squeeze",
            "filmback_width_3de",
            "filmback_height_3de",
            "distortion_model_3de",
            "is_downsampled",
            "is_upscaled",
            "codec",
            "raw_recording_available",
            "notes",
            "make_notes",
            "tracking_workflow",
        }
        assert set(data.keys()) == expected_keys
        assert data["image_format"] == "HD"

    @pytest.mark.django_db
    def test_get_format_details_not_found(self, client):
        """
        When we get a make that does not exist should get a 404
        """
        res = client.get(reverse("format", args=[9999]))

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_patch_forat_details(self, admin_client, single_format):
        """
        We should be able to update format details
        """
        update = {"image_format": "2K"}
        res = admin_client.patch(
            reverse("format", args=[single_format.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 200
        data = res.json()

        assert "success" in data

        # Confirm the database record was also updated
        single_format.refresh_from_db()
        assert single_format.image_format == "2K"

    @pytest.mark.django_db
    def test_patch_format_details_not_authenticated(self, client, single_format):
        """
        We can not update a format if we are not logged in
        """
        update = {"image_format": "2K"}
        res = client.patch(
            reverse("format", args=[single_format.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 401
        res_data = res.json()
        assert res_data["error"] == "Login required"

    @pytest.mark.django_db
    def test_patch_format_details_not_admin(self, client, single_format, regular_user):
        """
        Regular users are not allowd to update formats
        """
        # We can use our regular user fixture to log in
        client.force_login(regular_user)

        update = {
            "image_format": "2K",
        }

        res = client.patch(
            reverse("format", args=[single_format.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 403
        res_data = res.json()
        assert res_data["error"] == "Permission denied!"

    @pytest.mark.django_db
    def test_delete_format(self, admin_client, single_format):
        """
        We should be able to delete a format
        """
        format_id = single_format.id
        res = admin_client.delete(reverse("format", args=[single_format.id]))

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data

        # Check the database to make sure the record was deleted
        assert not Format.objects.filter(id=format_id).exists()

    @pytest.mark.django_db
    def test_delete_format_not_found(self, admin_client):
        """
        If we try to delete a format that does not exists we should get a 404
        """
        res = admin_client.delete(reverse("format", args=[999]))

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_delete_format_not_authenticated(self, client, single_format):
        """
        We can not delete a format if we are not logged in
        """
        format_id = single_format.id
        res = client.delete(reverse("format", args=[format_id]))

        assert res.status_code == 401

        data = res.json()
        assert data["error"] == "Login required"

    @pytest.mark.django_db
    def test_delete_format_not_admin(self, client, single_format, regular_user):
        """
        Regular users are not allowed to delete formats
        """
        format_id = single_format.id

        # We use our regular user fixture to log in
        client.force_login(regular_user)
        res = client.delete(reverse("format", args=[format_id]))

        assert res.status_code == 403

        data = res.json()
        assert data["error"] == "Permission denied!"


class TestFormatsSearchView:
    @pytest.mark.django_db
    def test_search_formats(self, client, multiple_formats):
        """
        We should be able to search formats based on their various fields
        """
        # TODO: This could use some abstraction
        res = client.get(reverse("search_formats", query={"make": "Arri"}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 2

        res = client.get(reverse("search_formats", query={"camera": "Alexa 35"}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 2
        assert data[0]["camera_model"] == "Alexa 35"

        res = client.get(reverse("search_formats", query={"source": "Sample Source"}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 4

        res = client.get(reverse("search_formats", query={"format": "4.6K"}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["image_format"] == "4.6K"

        res = client.get(reverse("search_formats", query={"image_aspect": "16:9"}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["image_aspect"] == "16:9"

        res = client.get(reverse("search_formats", query={"sensor_width": 9.01}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["sensor_width"] == 9.01

        res = client.get(reverse("search_formats", query={"sensor_height": 9.5}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["sensor_height"] == 9.5

        res = client.get(reverse("search_formats", query={"image_width": 2048}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["image_width"] == 2048

        res = client.get(reverse("search_formats", query={"image_height": 1080}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["image_height"] == 1080

        res = client.get(reverse("search_formats", query={"is_anamorphic": True}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["is_anamorphic"] is True

        res = client.get(reverse("search_formats", query={"anamorphic_squeeze": 2.0}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["anamorphic_squeeze"] == 2.0

        res = client.get(reverse("search_formats", query={"is_desqueezed": True}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["is_desqueezed"] is True

        res = client.get(reverse("search_formats", query={"pixel_aspect": 1.0}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 4
        assert data[0]["pixel_aspect"] == 1.0

        res = client.get(reverse("search_formats", query={"filmback_width_3de": 16.90}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["filmback_width_3de"] == 16.90

        res = client.get(reverse("search_formats", query={"filmback_height_3de": 4.75}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["filmback_height_3de"] == 4.75

        res = client.get(
            reverse("search_formats", query={"distortion_model_3de": "anamorphic"})
        )
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert "anamorphic" in data[0]["distortion_model_3de"].lower()

        res = client.get(reverse("search_formats", query={"is_downsampled": True}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["is_downsampled"] is True

        res = client.get(reverse("search_formats", query={"is_upscaled": True}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["is_upscaled"] is True

        res = client.get(reverse("search_formats", query={"codec": "ProRes"}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["codec"] == "ProRes"

        res = client.get(
            reverse("search_formats", query={"raw_recording_available": False})
        )
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["raw_recording_available"] is False

        res = client.get(reverse("search_formats", query={"notes": "A sample note"}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 1
        assert data[0]["notes"] == "A sample note"

        res = client.get(reverse("search_formats", query={"make_notes": "quality"}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 2
        assert "quality" in data[0]["make_notes"]

        res = client.get(
            reverse("search_formats", query={"tracking_workflow": "adjusted"})
        )
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 3
        assert "adjusted" in data[0]["tracking_workflow"]

    def test_search_formats_return_value(self, client, multiple_formats):
        """
        Formats should return a dict
        """
        res = client.get(reverse("search_formats", query={"make": "Arri"}))
        assert res.status_code == 200

        # Check that we found the correct number of records
        data = res.json()
        assert len(data) == 2

        # Check the dict strucutre
        expected_keys = {
            "id",
            "camera",
            "camera_model",
            "make_name",
            "source",
            "image_format",
            "image_aspect",
            "format_name",
            "sensor_width",
            "sensor_height",
            "image_width",
            "image_height",
            "pixel_aspect",
            "is_anamorphic",
            "is_desqueezed",
            "anamorphic_squeeze",
            "filmback_width_3de",
            "filmback_height_3de",
            "distortion_model_3de",
            "is_downsampled",
            "is_upscaled",
            "codec",
            "raw_recording_available",
            "notes",
            "make_notes",
            "tracking_workflow",
        }
        assert set(data[0].keys()) == expected_keys

    @pytest.mark.django_db
    def test_search_formats_case_insensitive(self, client, multiple_formats):
        """
        Search should be case insensitive
        """
        res = client.get(reverse("search_formats", query={"make": "red"}))

        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert len(data) == 2
        assert data[0]["make_name"] == "RED"

    @pytest.mark.django_db
    def test_search_formats_no_results(self, client, multiple_formats):
        """
        If no results are found we should get an empty string
        """
        res = client.get(reverse("search_formats", query={"make": "fake make"}))

        assert res.status_code == 200

        # Check that we got an empty list
        data = res.json()
        assert data == []

    @pytest.mark.django_db
    def test_search_formats_no_query(self, client, multiple_formats):
        """
        No query should return an error
        """
        res = client.get(reverse("search_formats"))

        # TODO: Shouldn't this return 400?
        assert res.status_code == 200

        # Check that we got an error
        data = res.json()
        assert "error" in data
        assert data["error"] == "No query provided"

    @pytest.mark.django_db
    def test_search_formats_empty_query(self, client, multiple_formats):
        """
        Empty queries should return an error?
        """
        res = client.get(reverse("search_formats", query={"make": ""}))

        # TODO: Shouldn't this return 400?
        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert "error" in data
        assert data["error"] == "No query provided"
