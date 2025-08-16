from pprint import pprint
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from sources.models import Source
from django.test.client import encode_multipart, BOUNDARY

User = get_user_model()


class TestSourcesListView:
    """
    Tests for the Source list view
    """

    @pytest.mark.django_db
    def test_get_all_sources_empty(self, client):
        """
        Test getting all sources when we don't have any records in the DB
        """

        res = client.get(reverse("sources"))

        assert res.status_code == 200
        data = res.json()
        assert data == []

    @pytest.mark.django_db
    def test_get_all_sources_with_data(self, client, multiple_sources):
        """
        Test getting all sources when we have records in the DB
        """

        res = client.get(reverse("sources"))

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 4

        # Check the names
        sources = [source["name"] for source in data]
        assert "Source-A" in sources
        assert "Source-B" in sources
        assert "Source-C" in sources
        assert "Source-CD" in sources

        for source_data in data:
            expected_keys = {
                "id",
                "name",
                "url",
                "file_name",
                "note",
            }
            assert set(source_data.keys()) == expected_keys

    @pytest.mark.django_db
    def test_create_source(self, admin_client):
        """
        Can we create a source?
        """
        data = {
            "name": "New Source",
            "url": "http://www.new_source.com",
            "file_name": "a_new_source.pdf",
            "note": "the best source yet!",
        }

        res = admin_client.post(
            reverse("sources"),
            data,
            content_type="application/json",
        )

        res_data = res.json()
        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data
        assert "source" in res_data

        # Check the database to make sure the record was created
        source = Source.objects.get(id=res_data["source"]["id"])
        assert source.name == "New Source"
        assert source.url == "http://www.new_source.com"
        assert source.file_name == "a_new_source.pdf"
        assert source.note == "the best source yet!"

    @pytest.mark.django_db
    def test_create_source_with_missing_fields(self, admin_client):
        """
        Missing required fields should return an error
        """
        # TODO: Test multiple missing fields this only checks for make
        data = {
            "name": "Missing Fields Source",
        }

        res = admin_client.post(
            reverse("sources"),
            data,
            content_type="application/json",
        )

        assert res.status_code == 400
        res_data = res.json()
        assert "error" in res_data
        assert "url is required" in res_data["error"]

    @pytest.mark.django_db
    def test_create_source_not_authenticated(
        self, client, single_make, sample_uploaded_file
    ):
        """
        If we did not log in we can not create a Source
        """
        data = {
            "name": "New Source",
            "url": "http://www.new_source.com",
            "file_name": "a_new_source.pdf",
            "notes": "the best source yet!",
        }

        res = client.post(
            reverse("sources"),
            data,
            content_type="application/json",
        )

        assert res.status_code == 401
        res_data = res.json()
        assert res_data["error"] == "Login required"

    @pytest.mark.django_db
    def test_create_source_not_admin(self, regular_user, client, single_make):
        """
        Regular users are not allowed to create Makes
        """

        # We can use our regular user fixture to log in
        client.force_login(regular_user)

        data = {
            "name": "New Source",
            "url": "http://www.new_source.com",
            "file_name": "a_new_source.pdf",
            "notes": "the best source yet!",
        }

        res = client.post(
            reverse("sources"),
            data,
            content_type="application/json",
        )

        assert res.status_code == 403
        res_data = res.json()
        assert res_data["error"] == "Permission denied!"


class TestSourceDetailsView:
    """
    Tests for the Source details view
    """

    @pytest.mark.django_db
    def test_get_source_details(self, single_source, client):
        """
        Test that we can get a Source details
        """
        res = client.get(reverse("source", args=[single_source.id]))

        assert res.status_code == 200

        data = res.json()
        expected_keys = {
            "id",
            "name",
            "url",
            "file_name",
            "note",
        }
        assert set(data.keys()) == expected_keys
        assert data["name"] == "Sample Source"

    @pytest.mark.django_db
    def test_get_source_details_not_found(self, client):
        """
        When we get a make that does not exist should get a 404
        """
        res = client.get(reverse("source", args=[9999]))

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_patch_source_details(self, admin_client, single_source):
        """
        We should be able to update source details
        """
        update = {"name": "Updated Source"}
        res = admin_client.patch(
            reverse("source", args=[single_source.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 200
        data = res.json()

        assert "success" in data

        # Confirm the database record was also updated
        single_source.refresh_from_db()
        assert single_source.name == "Updated Source"

    @pytest.mark.django_db
    def test_patch_source_details_not_authenticated(self, client, single_source):
        """
        We can not update a source if we are not logged in
        """
        update = {"name": "Updated Source"}
        res = client.patch(
            reverse("source", args=[single_source.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 401
        res_data = res.json()
        assert res_data["error"] == "Login required"

    @pytest.mark.django_db
    def test_patch_source_details_not_admin(self, client, single_source, regular_user):
        """
        Regular users are not allowd to update sources
        """
        # We can use our regular user fixture to log in
        client.force_login(regular_user)

        update = {
            "name": "Regular User Source",
        }

        res = client.patch(
            reverse("source", args=[single_source.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 403
        res_data = res.json()
        assert res_data["error"] == "Permission denied!"

    @pytest.mark.django_db
    def test_delete_source(self, admin_client, single_source):
        """
        We should be able to delete a source
        """
        source_id = single_source.id
        res = admin_client.delete(reverse("source", args=[single_source.id]))

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data

        # Check the database to make sure the record was deleted
        assert not Source.objects.filter(id=source_id).exists()

    @pytest.mark.django_db
    def test_delete_source_not_found(self, admin_client):
        """
        If we try to delete a source that does not exists we should get a 404
        """
        res = admin_client.delete(reverse("source", args=[999]))

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_delete_source_not_authenticated(self, client, single_source):
        """
        We can not delete a source if we are not logged in
        """
        source_id = single_source.id
        res = client.delete(reverse("source", args=[source_id]))

        assert res.status_code == 401

        data = res.json()
        assert data["error"] == "Login required"

    @pytest.mark.django_db
    def test_delete_source_not_admin(self, client, single_source, regular_user):
        """
        Regular users are not allowed to delete sources
        """
        source_id = single_source.id

        # We use our regular user fixture to log in
        client.force_login(regular_user)
        res = client.delete(reverse("source", args=[source_id]))

        assert res.status_code == 403

        data = res.json()
        assert data["error"] == "Permission denied!"


class TestwSourcesSearchView:
    @pytest.mark.django_db
    def test_search_sources(self, client, multiple_sources):
        """
        We should be able to search makes based on their names
        """
        res = client.get(reverse("search_sources", query={"q": "Source-A"}))

        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert len(data) == 1
        assert data[0]["name"] == "Source-A"

        # Check the dict strucutre
        expected_keys = {
            "id",
            "name",
            "url",
            "file_name",
            "note",
        }

        assert set(data[0].keys()) == expected_keys

    @pytest.mark.django_db
    def test_search_sources_partial(self, client, multiple_sources):
        """
        If we search for a part of a name we should get all results that contain that
        partial string
        """

        res = client.get(reverse("search_sources", query={"q": "Source-C"}))

        assert res.status_code == 200

        # Check that we found the correct makes
        data = res.json()
        assert len(data) == 2
        names = [source["name"] for source in data]
        assert "Source-C" in names
        assert "Source-CD" in names

    @pytest.mark.django_db
    def test_search_source_case_insensitive(self, client, multiple_sources):
        """
        Search should be case insensitive
        """
        res = client.get(reverse("search_sources", query={"q": "source-a"}))

        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert len(data) == 1
        assert data[0]["name"] == "Source-A"

    @pytest.mark.django_db
    def test_search_sources_no_results(self, client, multiple_sources):
        """
        If no results are found we should get an empty string
        """
        res = client.get(reverse("search_sources", query={"q": "fake source"}))

        assert res.status_code == 200

        # Check that we got an empty list
        data = res.json()
        assert data == []

    @pytest.mark.django_db
    def test_search_sources_no_query(self, client, multiple_sources):
        """
        No query should return an error
        """
        res = client.get(reverse("search_sources"))

        # TODO: Shouldn't this return 400?
        assert res.status_code == 200

        # Check that we got an error
        data = res.json()
        assert "error" in data
        assert data["error"] == "No query provided"

    @pytest.mark.django_db
    def test_search_sources_empty_query(self, client, multiple_sources):
        """
        Empty queries should return an error?
        """
        res = client.get(reverse("search_sources", query={"q": ""}))

        # TODO: Shouldn't this return 400?
        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert "error" in data
        assert data["error"] == "No query provided"
