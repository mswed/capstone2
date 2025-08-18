import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()


class TestProjectsListView:
    """
    Tests for the Formats list view
    """

    @pytest.mark.django_db
    def test_get_all_projects_empty(self, client):
        """
        Test getting all formats when we don't have any records in the DB
        """

        res = client.get(reverse("projects"))

        assert res.status_code == 200
        data = res.json()
        assert data == []

    @pytest.mark.django_db
    def test_get_all_projects_with_data(self, client, multiple_projects):
        """
        Test getting all projects when we have records in the DB
        """

        res = client.get(reverse("projects"))

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 2

        # Check the names
        names = [name["name"] for name in data]
        assert "One Piece" in names
        assert "Daredevil" in names

        for format_data in data:
            expected_keys = {
                "id",
                "name",
                "project_type",
                "description",
                "poster_path",
                "release_date",
                "adult",
                "tmdb_id",
                "tmdb_original_name",
                "genres",
                "rating",
            }
            assert set(format_data.keys()) == expected_keys

    @pytest.mark.django_db
    def test_create_project(self, admin_client):
        """
        Can we create a project?
        """

        # At the moment we can only create a project based on a TMBD id
        data = {
            "tmdb_id": 803796,
            "project_type": "feature",
        }

        res = admin_client.post(
            reverse("projects"), data, content_type="application/json"
        )

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data

        # Check the database to make sure the record was created
        project = Project.objects.get(id=res_data["project"]["id"])
        assert project.name == "KPop Demon Hunters"
        assert "Rumi, Mira and Zoey" in project.description

    @pytest.mark.django_db
    def test_create_format_with_missing_fields(self, admin_client):
        """
        Missing required fields should return an error
        """
        data = {}
        res = admin_client.post(
            reverse("projects"), data, content_type="application/json"
        )

        assert res.status_code == 400
        res_data = res.json()
        assert "error" in res_data
        assert "tmdb_id is required" in res_data["error"]

        data = {"tmdb_id": 123456}
        res = admin_client.post(
            reverse("projects"), data, content_type="application/json"
        )

        assert res.status_code == 400
        res_data = res.json()
        assert "error" in res_data
        assert "project_type is required" in res_data["error"]

    @pytest.mark.django_db
    def test_create_project_not_authenticated(self, client):
        """
        If we did not log in we can not create a project
        """
        data = {
            "tmdb_id": 803796,
            "project_type": "feature",
        }

        res = client.post(reverse("projects"), data, content_type="application/json")

        assert res.status_code == 401
        res_data = res.json()
        assert res_data["error"] == "Login required"

    @pytest.mark.django_db
    def test_create_project_not_admin(self, regular_user, client):
        """
        Regular users are should also be allowed to create projects
        """
        # We can use our regular user fixture to log in
        client.force_login(regular_user)

        data = {
            "tmdb_id": 37136,
            "project_type": "feature",
        }

        res = client.post(reverse("projects"), data, content_type="application/json")

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data

        # Check the database to make sure the record was created
        project = Project.objects.get(id=res_data["project"]["id"])
        assert project.name == "The Naked Gun: From the Files of Police Squad!"
        assert "bumbling Lieutenant Frank Drebin" in project.description


class TestProjectDetailsView:
    """
        Tests for the Project details view
    db"""

    @pytest.mark.django_db
    def test_get_project_details(self, single_project, client):
        """
        Test that we can get a projects's details
        """
        res = client.get(reverse("project", args=[single_project.id]))

        assert res.status_code == 200

        data = res.json()
        expected_keys = {
            "id",
            "name",
            "project_type",
            "description",
            "poster_path",
            "release_date",
            "adult",
            "tmdb_id",
            "tmdb_original_name",
            "genres",
            "rating",
            "cameras",  # Details has these additional fields
            "formats",
        }
        assert set(data.keys()) == expected_keys
        assert data["name"] == "Edge of Tomorrow"

    @pytest.mark.django_db
    def test_get_project_details_not_found(self, client):
        """
        When we get a project that does not exist should get a 404
        """
        res = client.get(reverse("project", args=[9999]))

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_patch_project_details(self, admin_client, single_project):
        """
        We should be able to update project details
        """
        update = {"name": "Edge of Tomorrow Updated"}
        res = admin_client.patch(
            reverse("project", args=[single_project.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 200
        data = res.json()

        assert "success" in data

        # Confirm the database record was also updated
        single_project.refresh_from_db()
        assert single_project.name == "Edge of Tomorrow Updated"

    @pytest.mark.django_db
    def test_patch_project_details_not_authenticated(self, client, single_project):
        """
        We can not update a project if we are not logged in
        """
        update = {"name": "Edge of Tomorrow Not Logged In"}
        res = client.patch(
            reverse("project", args=[single_project.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 401
        res_data = res.json()
        assert res_data["error"] == "Login required"

    @pytest.mark.django_db
    def test_patch_project_details_not_admin(
        self, client, single_project, regular_user
    ):
        """
        Regular users are not allowd to update projects
        """
        # We can use our regular user fixture to log in
        client.force_login(regular_user)

        update = {
            "name": "Edge of Tomorrow Regular User",
        }

        res = client.patch(
            reverse("project", args=[single_project.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 403
        res_data = res.json()
        assert res_data["error"] == "Permission denied!"

    @pytest.mark.django_db
    def test_delete_project(self, admin_client, single_project):
        """
        We should be able to delete a project
        """
        project_id = single_project.id
        res = admin_client.delete(reverse("project", args=[single_project.id]))

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data

        # Check the database to make sure the record was deleted
        assert not Project.objects.filter(id=project_id).exists()

    @pytest.mark.django_db
    def test_delete_project_not_found(self, admin_client):
        """
        If we try to delete a project that does not exists we should get a 404
        """
        res = admin_client.delete(reverse("project", args=[999]))

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_delete_project_not_authenticated(self, client, single_project):
        """
        We can not delete a project if we are not logged in
        """
        project_id = single_project.id
        res = client.delete(reverse("project", args=[project_id]))

        assert res.status_code == 401

        data = res.json()
        assert data["error"] == "Login required"

    @pytest.mark.django_db
    def test_delete_project_not_admin(self, client, single_project, regular_user):
        """
        Regular users are not allowed to delete projects (yet)
        """
        project_id = single_project.id

        # We use our regular user fixture to log in
        client.force_login(regular_user)
        res = client.delete(reverse("format", args=[project_id]))

        assert res.status_code == 403

        data = res.json()
        assert data["error"] == "Permission denied!"


class TestProjectsSearchView:
    @pytest.mark.django_db
    def test_search_projects(self, client, multiple_projects):
        """
        We should be able to search projects based on name
        """
        res = client.get(reverse("search_projects", query={"q": "Daredevil"}))
        assert res.status_code == 200

        data = res.json()

        # We expect to have local and remote projects
        assert "projects" in data
        assert "local" in data["projects"]
        assert "remote" in data["projects"]

        # Confirm that we have one local project
        assert len(data["projects"]["local"]) == 1
        assert data["projects"]["local"][0]["name"] == "Daredevil"

        # Confirm that we got a dict
        expected_keys = {
            "id",
            "name",
            "project_type",
            "description",
            "poster_path",
            "release_date",
            "adult",
            "tmdb_id",
            "tmdb_original_name",
            "genres",
            "rating",
        }

        assert set(data["projects"]["local"][0].keys()) == expected_keys

        # Confirm that we have a few remote projects
        assert len(data["projects"]["local"]) > 0
        assert "daredevil" in data["projects"]["remote"][0]["name"].lower()

    @pytest.mark.django_db
    def test_search_projects_case_insensitive(self, client, multiple_projects):
        """
        Search should be case insensitive
        """
        res = client.get(reverse("search_projects", query={"q": "one piece"}))

        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert len(data["projects"]["local"]) == 1
        assert data["projects"]["local"][0]["name"] == "One Piece"

    @pytest.mark.django_db
    def test_search_projects_no_results(self, client, multiple_formats):
        """
        If no results are found we should get an empty string
        """
        res = client.get(reverse("search_projects", query={"q": "fjkldasjf"}))

        assert res.status_code == 200

        # Check that we got an empty list
        data = res.json()

        # We expect to have local and remote projects
        assert "projects" in data
        assert "local" in data["projects"]
        assert "remote" in data["projects"]
        assert len(data["projects"]["local"]) == 0
        assert len(data["projects"]["remote"]) == 0

    @pytest.mark.django_db
    def test_search_projects_no_query(self, client, multiple_projects):
        """
        No query should return an error
        """
        res = client.get(reverse("search_projects"))

        # TODO: Shouldn't this return 400?
        assert res.status_code == 200

        # Check that we got an error
        data = res.json()
        assert "error" in data
        assert data["error"] == "No query provided"

    @pytest.mark.django_db
    def test_search_projects_empty_query(self, client, multiple_projects):
        """
        Empty queries should return an error?
        """
        res = client.get(reverse("search_formats", query={"q": ""}))

        # TODO: Shouldn't this return 400?
        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert "error" in data
        assert data["error"] == "No query provided"
