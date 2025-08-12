from pprint import pprint
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from makes.models import Make
from cameras.models import Camera
from django.test.client import encode_multipart, BOUNDARY

User = get_user_model()


class TestCamerasListView:
    """
    Tests for the Camera list view
    """

    @pytest.mark.django_db
    def test_get_all_cameras_empty(self, client):
        """
        Test getting all cameras when we don't have any records in the DB
        """

        res = client.get(reverse("cameras"))

        assert res.status_code == 200
        data = res.json()
        assert data == []

    @pytest.mark.django_db
    def test_get_all_cameras_with_data(self, client, multiple_cameras):
        """
        Test getting all cameras when we have records in the DB
        """

        res = client.get(reverse("cameras"))

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 4

        # Check the names
        models = [cam["model"] for cam in data]
        assert "Alexa 35" in models
        assert "Alexa Mini LF" in models
        assert "KOMODO" in models
        assert "KOMODO-X" in models

        for camera_data in data:
            expected_keys = {
                "id",
                "make",
                "make_name",
                "model",
                "sensor_size",
                "sensor_type",
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
            assert set(camera_data.keys()) == expected_keys

    @pytest.mark.django_db
    def test_create_camera_no_image(self, admin_client, single_make):
        """
        Can we create a camera without an image?
        """
        data = {
            "make": single_make.id,
            "model": "Alexa Mini",
            "sensor_type": "Super 35 format ARRI ALEV III CMOS sensor with Bayer pattern color filter array",
            "sensor_size": "Super 35",
            "max_filmback_width": 28.25,
            "max_filmback_height": 18.17,
            "max_image_width": 3424,
            "max_image_height": 2202,
            "min_frame_rate": 0.75,
            "max_frame_rate": 120,
        }

        res = admin_client.post(reverse("cameras"), data)

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data
        assert "camera_id" in res_data

        # Check the database to make sure the record was created
        camera = Camera.objects.get(id=res_data["camera_id"])
        print(camera)
        pprint(camera.as_dict())
        assert camera.sensor_size == "Super 35"
        assert camera.max_image_width == 3424
        assert camera.max_frame_rate == 120

    @pytest.mark.django_db
    def test_create_camera_with_image(
        self, admin_client, single_make, sample_uploaded_file
    ):
        """
        Can we create a camera with an image?
        """
        data = {
            "make": single_make.id,
            "model": "Alexa Mini With Image",
            "sensor_type": "Super 35 format ARRI ALEV III CMOS sensor with Bayer pattern color filter array",
            "sensor_size": "Super 35",
            "max_filmback_width": 28.25,
            "max_filmback_height": 18.17,
            "max_image_width": 3424,
            "max_image_height": 2202,
            "min_frame_rate": 0.75,
            "max_frame_rate": 120,
            "image": sample_uploaded_file,
        }
        res = admin_client.post(reverse("cameras"), data)

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data
        assert "camera_id" in res_data

        # Check the database to make sure the record was created
        camera = Camera.objects.get(model="Alexa Mini With Image")
        assert camera.image is not None
        assert "test_uploaded_image" in camera.image.name

    @pytest.mark.django_db
    def test_create_camera_with_missing_fields(self, admin_client):
        """
        Missing required fields should return an error
        """
        # TODO: Test multiple missing fields this only checks for make
        data = {
            "model": "Incomplete Camera",
        }
        res = admin_client.post(reverse("cameras"), data)

        assert res.status_code == 400
        res_data = res.json()
        assert "error" in res_data
        assert "make is required" in res_data["error"]

    @pytest.mark.django_db
    def test_create_camera_not_authenticated(
        self, client, single_make, sample_uploaded_file
    ):
        """
        If we did not log in we can not create a Camera
        """
        data = {
            "make": single_make,
            "model": "Alexa Mini With Image",
            "sensor_type": "Super 35 format ARRI ALEV III CMOS sensor with Bayer pattern color filter array",
            "sensor_size": "Super 35",
            "max_filmback_width": 28.25,
            "max_filmback_height": 18.17,
            "max_image_width": 3424,
            "max_image_height": 2202,
            "min_frame_rate": 0.75,
            "max_frame_rate": 120,
            "image": sample_uploaded_file,
        }

        res = client.post(reverse("cameras"), data)

        assert res.status_code == 401
        res_data = res.json()
        assert res_data["error"] == "Login required"

    @pytest.mark.django_db
    def test_create_camera_not_admin(self, regular_user, client, single_make):
        """
        Regular users are not allowed to create Makes
        """

        # We can use our regular user fixture to log in
        client.force_login(regular_user)

        data = {
            "make": single_make,
            "model": "Alexa Mini With Image",
            "sensor_type": "Super 35 format ARRI ALEV III CMOS sensor with Bayer pattern color filter array",
            "sensor_size": "Super 35",
            "max_filmback_width": 28.25,
            "max_filmback_height": 18.17,
            "max_image_width": 3424,
            "max_image_height": 2202,
            "min_frame_rate": 0.75,
            "max_frame_rate": 120,
        }

        res = client.post(reverse("cameras"), data)

        assert res.status_code == 403
        res_data = res.json()
        assert res_data["error"] == "Permission denied!"


class TestCameraDetailsView:
    """
    Tests for the Camera details view
    """

    @pytest.mark.django_db
    def test_get_camera_details(self, single_camera, client):
        """
        Test that we can get a Camera details
        """
        res = client.get(reverse("camera", args=[single_camera.id]))

        assert res.status_code == 200

        data = res.json()
        expected_keys = {
            "id",
            "make",
            "make_name",
            "model",
            "sensor_size",
            "sensor_type",
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
        assert set(data.keys()) == expected_keys
        assert data["model"] == "KOMODO"
        assert data["formats"] == []

    @pytest.mark.django_db
    def test_get_camera_details_not_found(self, client):
        """
        When we get a make that does not exist should get a 404
        """
        res = client.get(reverse("camera", args=[9999]))

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_patch_camera_details_no_image(self, admin_client, single_camera):
        """
        We should be able to update camera details even if it has no image
        """
        update = {"model": "Updated Model"}
        res = admin_client.patch(
            reverse("camera", args=[single_camera.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 200
        data = res.json()

        assert "success" in data

        # Confirm the database record was also updated
        single_camera.refresh_from_db()
        assert single_camera.model == "Updated Model"

    @pytest.mark.django_db
    def test_patch_camera_details_with_image(
        self, admin_client, single_camera, sample_uploaded_file
    ):
        """
        We should be able to update a camra with a new image
        """
        updated_data = {
            "model": "Updated Model",
            "image": sample_uploaded_file,
        }

        # Because we are passing an image we need to encode the data. We can not
        # just send json
        content = encode_multipart(BOUNDARY, updated_data)
        # And set it to a multipart form
        content_type = f"multipart/form-data; boundary={BOUNDARY}"

        res = admin_client.patch(
            reverse("camera", args=[single_camera.id]),
            content,
            content_type=content_type,
        )

        assert res.status_code == 200
        data = res.json()

        assert "success" in data

        # Confirm the database record was also updated
        single_camera.refresh_from_db()
        assert single_camera.model == "Updated Model"
        assert single_camera.image is not None
        assert "test_uploaded_image" in single_camera.image.name

    @pytest.mark.django_db
    def test_patch_camera_details_not_authenticated(self, client, single_camera):
        """
        We can not update a camera if we are not logged in
        """
        update = {"model": "Updated Model"}
        res = client.patch(
            reverse("camera", args=[single_camera.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 401
        res_data = res.json()
        assert res_data["error"] == "Login required"

    @pytest.mark.django_db
    def test_patch_camera_details_not_admin(self, client, single_camera, regular_user):
        """
        Regular users are not allowd to update cameras
        """
        # We can use our regular user fixture to log in
        client.force_login(regular_user)

        update = {
            "model": "Regular User Camera",
        }

        res = client.patch(
            reverse("camera", args=[single_camera.id]),
            update,
            content_type="application/json",
        )

        assert res.status_code == 403
        res_data = res.json()
        assert res_data["error"] == "Permission denied!"

    @pytest.mark.django_db
    def test_delete_camera(self, admin_client, single_camera):
        """
        We should be able to delete a camera
        """
        camera_id = single_camera.id
        res = admin_client.delete(reverse("camera", args=[single_camera.id]))

        assert res.status_code == 200
        res_data = res.json()
        assert "success" in res_data

        # Check the database to make sure the record was deleted
        assert not Camera.objects.filter(id=camera_id).exists()

    @pytest.mark.django_db
    def test_delete_camera_not_found(self, admin_client):
        """
        If we try to delete a camera that does not exists we should get a 404
        """
        res = admin_client.delete(reverse("camera", args=[999]))

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_delete_camera_not_authenticated(self, client, single_camera):
        """
        We can not delete a make if we are not logged in
        """
        camera_id = single_camera.id
        res = client.delete(reverse("camera", args=[camera_id]))

        assert res.status_code == 401

        data = res.json()
        assert data["error"] == "Login required"

    @pytest.mark.django_db
    def test_delete_camera_not_admin(self, client, single_camera, regular_user):
        """
        Regular users are not allowed to delete cameras
        """
        camera_id = single_camera.id

        # We use our regular user fixture to log in
        client.force_login(regular_user)
        res = client.delete(reverse("camera", args=[camera_id]))

        assert res.status_code == 403

        data = res.json()
        assert data["error"] == "Permission denied!"


class TestCamerasSearchView:
    @pytest.mark.django_db
    def test_search_cameras(self, client, multiple_cameras):
        """
        We should be able to search makes based on their names
        """
        res = client.get(reverse("search_cameras", query={"q": "Alexa 35"}))

        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert len(data) == 1
        assert data[0]["model"] == "Alexa 35"

        # Check the dict strucutre
        expected_keys = {
            "id",
            "make",
            "make_name",
            "model",
            "sensor_size",
            "sensor_type",
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
        assert set(data[0].keys()) == expected_keys

    @pytest.mark.django_db
    def test_search_cameras_partial(self, client, multiple_cameras):
        """
        If we search for a part of a name we should get all results that contain that
        partial string
        """

        res = client.get(reverse("search_cameras", query={"q": "Alex"}))

        assert res.status_code == 200

        # Check that we found the correct makes
        data = res.json()
        assert len(data) == 2
        names = [cam["model"] for cam in data]
        assert "Alexa 35" in names
        assert "Alexa Mini LF" in names

    @pytest.mark.django_db
    def test_search_cameras_case_insensitive(self, client, multiple_cameras):
        """
        Search should be case insensitive
        """
        res = client.get(reverse("search_cameras", query={"q": "komodo"}))

        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert len(data) == 2
        assert data[0]["model"] == "KOMODO"

    @pytest.mark.django_db
    def test_search_cameras_no_results(self, client, multiple_cameras):
        """
        If no results are found we should get an empty string
        """
        res = client.get(reverse("search_cameras", query={"q": "fake model"}))

        assert res.status_code == 200

        # Check that we got an empty list
        data = res.json()
        assert data == []

    @pytest.mark.django_db
    def test_search_makes_no_query(self, client, multiple_cameras):
        """
        No query should return an error
        """
        res = client.get(reverse("search_cameras"))

        # TODO: Shouldn't this return 400?
        assert res.status_code == 200

        # Check that we got an error
        data = res.json()
        assert "error" in data
        assert data["error"] == "No query provided"

    @pytest.mark.django_db
    def test_search_cameras_empty_query(self, client, multiple_cameras):
        """
        Empty queries should return an error?
        """
        res = client.get(reverse("search_cameras", query={"q": ""}))

        # TODO: Shouldn't this return 400?
        assert res.status_code == 200

        # Check that we found the correct make
        data = res.json()
        assert "error" in data
        assert data["error"] == "No query provided"
