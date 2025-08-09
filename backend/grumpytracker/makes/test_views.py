import pytest
import json
from django.test import Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from PIL import Image
from io import BytesIO
from makes.models import Make
from .test_fixtures import (
    multiple_makes,
    sample_uploaded_file,
    regular_user,
    single_make,
)
from django.test.client import encode_multipart, BOUNDARY

User = get_user_model()


class TestMakeListView:
    """
    Tests for the Make list view
    """

    @pytest.mark.django_db
    def test_get_all_makes_empty(self, client):
        """
        Test getting all makes when we don't have any records in the DB
        """

        res = client.get(reverse("makes"))

        assert res.status_code == 200
        data = res.json()
        assert data == []

    @pytest.mark.django_db
    def test_get_all_makes_with_data(self, client, multiple_makes):
        """
        Test getting all makes when we don't have any records in the DB
        """

        res = client.get(reverse("makes"))

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 3

        # Check the names
        names = [make["name"] for make in data]
        assert "Canon" in names
        assert "Sony" in names
        assert "Panasonic" in names

        for make_data in data:
            expected_keys = {
                "id",
                "name",
                "website",
                "logo",
                "cameras_count",
            }
            assert set(make_data.keys()) == expected_keys

    @pytest.mark.django_db
    def test_create_make_no_logo(self, admin_client):
        data = {"name": "Arri", "website": "https://www.arri.com"}
        res = admin_client.post(reverse("makes"), data)

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data
        assert "make_id" in res_data

        # Check the database to make sure the record was created
        make = Make.objects.get(name="Arri")
        assert make.website == "https://www.arri.com"

    @pytest.mark.django_db
    def test_create_make_with_logo(self, admin_client, sample_uploaded_file):
        data = {
            "name": "Arri With Logo",
            "website": "https://www.arri.com",
            "logo": sample_uploaded_file,
        }
        res = admin_client.post(reverse("makes"), data)

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data
        assert "make_id" in res_data

        # Check the database to make sure the record was created
        make = Make.objects.get(name="Arri With Logo")
        assert make.logo is not None
        assert "test_uploaded_image" in make.logo.name

    @pytest.mark.django_db
    def test_create_make_with_missing_fields(self, admin_client):
        data = {
            "name": "Incomplete Make",
        }
        res = admin_client.post(reverse("makes"), data)

        assert res.status_code == 400
        res_data = res.json()
        assert "error" in res_data
        assert "website is required" in res_data["error"]

    @pytest.mark.django_db
    def test_create_make_not_authenticated(self, client):
        """
        If we did not log in we can not create a Make
        """
        data = {
            "name": "Not Authenticated Make",
            "website": "https://www.nam.com",
        }

        res = client.post(reverse("makes"), data)

        assert res.status_code == 401
        res_data = res.json()
        assert res_data["error"] == "Login required"

    @pytest.mark.django_db
    def test_create_make_not_admin(self, regular_user, client):
        """
        Regular users are not allowed to create Makes
        """

        # We can use our regular user fixture to log in
        client.force_login(regular_user)

        data = {
            "name": "Regular User Make",
            "website": "https://www.rum.com",
        }

        res = client.post(reverse("makes"), data)

        assert res.status_code == 403
        res_data = res.json()
        assert res_data["error"] == "Permission denied!"


class TestMakeDetailsView:
    """
    Tests for the Make details view
    """

    @pytest.mark.django_db
    def test_get_make_details(self, single_make, client):
        """
        Test that we can get a Make details
        """
        res = client.get(reverse("make", args=[single_make.id]))

        assert res.status_code == 200

        data = res.json()
        expected_keys = {"id", "name", "website", "logo", "cameras_count", "cameras"}
        assert set(data.keys()) == expected_keys
        assert data["name"] == "Sample Make"
        assert data["cameras"] == []

    @pytest.mark.django_db
    def test_get_make_details_not_found(self, client):
        """
        Test that we get a 404 when we look for a Make that does not exist
        """
        res = client.get(reverse("make", args=[9999]))

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_patch_make_details_no_logo(self, admin_client, single_make):
        update = {"name": "Updated Make", "website": "https://www.updated-make.com"}
        res = admin_client.patch(
            reverse("make", args=[single_make.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 200
        data = res.json()

        assert "success" in data

        # Confirm the database record was also updated
        single_make.refresh_from_db()
        assert single_make.name == "Updated Make"
        assert single_make.website == "https://www.updated-make.com"

    @pytest.mark.django_db
    def test_patch_make_details_with_logo(
        self, admin_client, single_make, sample_uploaded_file
    ):
        updated_data = {
            "name": "Updated Make",
            "website": "https://www.updated-make.com",
            "logo": sample_uploaded_file,
        }

        # Because we are passing an image we need to encode the data. We can not
        # just send json
        content = encode_multipart(BOUNDARY, updated_data)
        # And set it to a multipart form
        content_type = f"multipart/form-data; boundary={BOUNDARY}"

        res = admin_client.patch(
            reverse("make", args=[single_make.id]),
            content,
            content_type=content_type,
        )

        assert res.status_code == 200
        data = res.json()

        assert "success" in data

        # Confirm the database record was also updated
        single_make.refresh_from_db()
        assert single_make.name == "Updated Make"
        assert single_make.website == "https://www.updated-make.com"
        assert single_make.logo is not None
        assert "test_uploaded_image" in single_make.logo.name

    @pytest.mark.django_db
    def test_patch_make_details_not_authenticated(self, client, single_make):
        update = {"name": "Updated Make", "website": "https://www.updated-make.com"}
        res = client.patch(
            reverse("make", args=[single_make.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 401
        res_data = res.json()
        assert res_data["error"] == "Login required"

    @pytest.mark.django_db
    def test_patch_make_details_not_admin(self, client, single_make, regular_user):
        # We can use our regular user fixture to log in
        client.force_login(regular_user)

        update = {
            "name": "Regular User Make",
            "website": "https://www.rum.com",
        }

        res = client.patch(
            reverse("make", args=[single_make.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 403
        res_data = res.json()
        assert res_data["error"] == "Permission denied!"

    @pytest.mark.django_db
    def test_delete_make(self, admin_client, single_make):
        make_id = single_make.id
        res = admin_client.delete(reverse("make", args=[single_make.id]))

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data

        # Check the database to make sure the record was deleted
        assert not Make.objects.filter(id=make_id).exists()

    @pytest.mark.django_db
    def test_delete_make_not_found(self, admin_client):
        res = admin_client.delete(reverse("make", args=[999]))

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_delete_make_not_authenticated(self, client, single_make):
        make_id = single_make.id
        res = client.delete(reverse("make", args=[make_id]))

        assert res.status_code == 401

        data = res.json()
        assert data["error"] == "Login required"

    @pytest.mark.django_db
    def test_delete_make_not_admin(self, client, single_make, regular_user):
        make_id = single_make.id

        # We use our regular user fixture to log in
        client.force_login(regular_user)
        res = client.delete(reverse("make", args=[make_id]))

        assert res.status_code == 403

        data = res.json()
        assert data["error"] == "Permission denied!"


class TestMakesSearchView:
    @pytest.mark.django_db
    def test_search_makes(self, client, multiple_makes):
        res = client.get(reverse("search_makes", query={"q": "Canon"}))

        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert len(data) == 1
        assert data[0]["name"] == "Canon"

        # Check the dict strucutre
        expected_keys = {"id", "name", "website"}
        assert set(data[0].keys()) == expected_keys

    @pytest.mark.django_db
    def test_search_makes_partial(self, client, multiple_makes):
        # Create more makes for partial search
        (Make.objects.create(name="Canon EOS", website="https://www.canon.com"),)
        (Make.objects.create(name="Canon PowerShot", website="https://www.canon.com"),)

        res = client.get(reverse("search_makes", query={"q": "Canon"}))

        assert res.status_code == 200

        # Check that we found the correct makes
        data = res.json()
        assert len(data) == 3
        names = [make["name"] for make in data]
        assert "Canon" in names
        assert "Canon EOS" in names
        assert "Canon PowerShot" in names

    @pytest.mark.django_db
    def test_search_makes_case_insensitive(self, client, multiple_makes):
        res = client.get(reverse("search_makes", query={"q": "CANON"}))

        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert len(data) == 1
        assert data[0]["name"] == "Canon"

    @pytest.mark.django_db
    def test_search_makes_no_results(self, client, multiple_makes):
        res = client.get(reverse("search_makes", query={"q": "fake make"}))

        assert res.status_code == 200

        # Check that we got an empty list
        data = res.json()
        assert data == []

    @pytest.mark.django_db
    def test_search_makes_no_query(self, client, multiple_makes):
        res = client.get(reverse("search_makes"))

        assert res.status_code == 200

        # Check that we got an error
        data = res.json()
        assert "error" in data
        assert data["error"] == "No query provided"

    @pytest.mark.django_db
    def test_search_makes_empty_query(self, client, multiple_makes):
        res = client.get(reverse("search_makes", query={"q": ""}))

        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert "error" in data
        assert data["error"] == "No query provided"
