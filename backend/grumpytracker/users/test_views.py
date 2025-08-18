import pytest
from unittest.mock import patch
import json
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthView:
    """
    Tests for the AuthView (login/logout)
    """

    def test_login_success(self, client):
        """
        We should be able to log in
        """
        # Create a test user
        user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )

        login_data = {"username": "testuser", "password": "testpass123"}

        # Patch the token
        with patch("jwt.encode") as mock_jwt:
            mock_jwt.return_value = "fake_jwt_token"

            response = client.post(
                reverse("auth"),
                data=json.dumps(login_data),
                content_type="application/json",
            )

            assert response.status_code == 200
            data = response.json()
            assert "success" in data
            assert "user" in data
            assert "token" in data
            assert data["token"] == "fake_jwt_token"
            assert data["user"]["username"] == "testuser"

    def test_login_missing_username(self, client):
        """
        We can not log in without a username
        """
        login_data = {"password": "testpass123"}

        response = client.post(
            reverse("auth"),
            data=json.dumps(login_data),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Username and Password are required" in data["error"]

    def test_login_missing_password(self, client):
        """
        We can not log in without a password
        """
        login_data = {"username": "testuser"}

        response = client.post(
            reverse("auth"),
            data=json.dumps(login_data),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Username and Password are required" in data["error"]

    def test_login_invalid_credentials(self, client):
        """
        Login with wrong user or password fails
        """
        # Create a test user
        User.objects.create_user(
            username="testuser", password="correctpass", email="test@example.com"
        )

        login_data = {"username": "testuser", "password": "wrongpass"}

        response = client.post(
            reverse("auth"),
            data=json.dumps(login_data),
            content_type="application/json",
        )

        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert "Wrong username or password" in data["error"]

    def test_login_nonexistent_user(self, client):
        """
        Noneexistent users can not log in
        """
        login_data = {"username": "nonexistent", "password": "testpass123"}

        response = client.post(
            reverse("auth"),
            data=json.dumps(login_data),
            content_type="application/json",
        )

        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert "Wrong username or password" in data["error"]

    def test_logout_authenticated_user(self, client):
        """
        We can log out
        """
        user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        client.force_login(user)

        response = client.delete(reverse("auth"))

        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "Logout successful" in data["success"]

    def test_logout_unauthenticated_user(self, client):
        """
        We can not log out if we did not log in
        """
        response = client.delete(reverse("auth"))

        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Not logged in" in data["error"]


@pytest.mark.django_db
class TestUsersListView:
    """
    Tests for the UsersListView (list users/register)
    """

    def test_get_users_as_admin(self, client, admin_user):
        """
        Admin can see all users
        """
        # Create some test users
        User.objects.create_user(
            username="user1", email="user1@test.com", password="pass"
        )
        User.objects.create_user(
            username="user2", email="user2@test.com", password="pass"
        )

        client.force_login(admin_user)

        response = client.get(reverse("users"))

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2  # At least our test users
        assert all("id" in user and "name" in user for user in data)

    def test_user_registration_success(self, client):
        """
        A new user can register
        """
        registration_data = {
            "username": "newuser",
            "password": "newpass123",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
        }

        response = client.post(
            reverse("users"),
            data=json.dumps(registration_data),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "Created user newuser" in data["success"]
        assert "source_id" in data

        # Verify user was created
        user = User.objects.get(username="newuser")
        assert user.email == "new@example.com"
        assert user.first_name == "New"
        assert user.last_name == "User"

    def test_user_registration_missing_required_fields(self, client):
        """
        We must provide all required fields when registering
        """
        registration_data = {
            "username": "newuser",
            "password": "newpass123",
        }

        response = client.post(
            reverse("users"),
            data=json.dumps(registration_data),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "email is required" in data["error"]

    def test_user_registration_duplicate_username(self, client):
        """
        Username must be unique
        """
        # Create existing user
        User.objects.create_user(
            username="existinguser", email="existing@example.com", password="pass123"
        )

        registration_data = {
            "username": "existinguser",  # Duplicate username
            "password": "newpass123",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
        }

        response = client.post(
            reverse("users"),
            data=json.dumps(registration_data),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data


@pytest.mark.django_db
class TestUserDetailsView:
    """
    Tests for the UserDetailsView (get/update/delete user)
    """

    def test_get_user_details_as_owner(self, client):
        """
        A user can get their own details
        """
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="pass123",
            first_name="Test",
            last_name="User",
        )
        client.force_login(user)

        response = client.get(reverse("user", args=[user.id]))

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_user_details_as_admin(self, admin_client):
        """
        Admin can get ALL user details
        """
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="pass123"
        )

        response = admin_client.get(reverse("user", args=[user.id]))

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"

    def test_get_nonexistent_user(self, admin_client):
        """
        If we try to get a nonexistent user we get a 404
        """

        response = admin_client.get(reverse("user", args=[999999]))

        assert response.status_code == 404

    def test_patch_user_success(self, client):
        """
        Users can update their details
        """
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="pass123",
            first_name="Old",
            last_name="Name",
        )
        client.force_login(user)

        update_data = {
            "first_name": "New",
            "last_name": "Name",
            "email": "newemail@example.com",
        }

        response = client.patch(
            reverse("user", args=[user.id]),
            data=json.dumps(update_data),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "user" in data
        assert data["user"]["first_name"] == "New"
        assert data["user"]["email"] == "newemail@example.com"

        # Verify changes in database
        user.refresh_from_db()
        assert user.first_name == "New"
        assert user.email == "newemail@example.com"

    def test_patch_user_password(self, client):
        """
        Passwords are hashed when updated
        """
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="oldpass123"
        )
        client.force_login(user)

        update_data = {"password": "newpass123"}

        response = client.patch(
            reverse("user", args=[user.id]),
            data=json.dumps(update_data),
            content_type="application/json",
        )

        assert response.status_code == 200

        # Verify password was hashed (not stored as plain text)
        user.refresh_from_db()
        assert user.password != "newpass123"
        assert user.check_password("newpass123")

    def test_patch_user_invalid_field(self, client):
        """
        Invalid fields are ignored when updating the user
        """
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="pass123"
        )
        client.force_login(user)

        update_data = {"invalid_field": "should_be_ignored", "first_name": "Valid"}

        response = client.patch(
            reverse("user", args=[user.id]),
            data=json.dumps(update_data),
            content_type="application/json",
        )

        assert response.status_code == 200
        user.refresh_from_db()
        assert user.first_name == "Valid"
        assert not hasattr(user, "invalid_field")

    def test_delete_user_success(self, client):
        """
        A user can delete their own record
        """
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="pass123"
        )
        user_id = user.id
        client.force_login(user)

        response = client.delete(reverse("user", args=[user_id]))

        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "User deleted" in data["success"]

        # Verify user was deleted
        assert not User.objects.filter(id=user_id).exists()

    def test_delete_nonexistent_user(self, client, admin_user):
        """
        If a nonexistent is being deleted we get a 404
        """
        client.force_login(admin_user)

        response = client.delete(reverse("user", args=[999999]))

        assert response.status_code == 404
