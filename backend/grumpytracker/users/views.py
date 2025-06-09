from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from grumpytracker.utils import (
    validate_required_fields,
    login_required,
    require_owner_or_admin,
    require_admin,
)
from loguru import logger

from .models import User


@method_decorator(csrf_exempt, name="dispatch")
class AuthView(View):
    """
    A class to handle login and logout operations, this is what case where the
    class View system feels less intuitive (post and delete instead of login and logout).
    """

    def post(self, request):
        """
        This is our loging function
        """
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                # We did not get a user name or a password
                return JsonResponse(
                    {"error": "Username and Password are required"}, status=400
                )

            # Authenticate using Django's built in function
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # We got a user back
                if user.is_active:
                    # Django keeps record of active users, we'll use it cause it's built in
                    # but honestly it might be overkill at this point
                    login(request, user)
                    return JsonResponse(
                        {"success": "Log in successful", "user": user.as_dict()}
                    )
                else:
                    return JsonResponse({"error": "Account is disabled"}, status=403)
            else:
                return JsonResponse({"error": "Wrong username or password"}, status=401)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request):
        """
        This is the logout function
        """
        if request.user.is_authenticated:
            # We are logged in so log out
            logout(request)
            return JsonResponse({"success": "Logout successful"})
        else:
            return JsonResponse({"error": "Not logged in"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class UsersListView(View):
    """
    Handle users/ endpoint
    GET - Returns all of the users in the DB
    POST - Creates a new user
    """

    @method_decorator(require_admin)
    def get(self, request) -> JsonResponse:
        """
        Return all existing users. This is a protected route only availabe for admin
        """

        users = User.objects.all()
        data = []

        for user in users:
            data.append({"id": user.id, "name": user.username})

        return JsonResponse(data, safe=False)

    def post(self, request) -> JsonResponse:
        try:
            data = json.loads(request.body)

            # Validate our input
            error = validate_required_fields(
                data,
                [
                    "username",
                    "password",
                    "email",
                    "first_name",
                    "last_name",
                ],
            )
            if error:
                return JsonResponse({"error": error}, status=400)

            logger.info("Passed validation")

            # Note that we are using create_user here not just create
            # since this will hash the password for us
            user = User.objects.create_user(
                username=data.get("username"),
                password=data.get("password"),
                email=data.get("email"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                role=data.get("role"),
                studio=data.get("studio"),
            )

            if not user:
                return JsonResponse({"error": "Failed to create user"})

            return JsonResponse(
                {
                    "success": f"Created user {user.username}",
                    "source_id": user.id,
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailsView(LoginRequiredMixin, View):
    """
    Handle user/123 endpoint
    GET - Returns the full user's details
    PATH - Update a user
    DELETE - Delete a user
    """

    @method_decorator(require_owner_or_admin)
    def get(self, request, user_id: int) -> JsonResponse:
        """
        Get a user by its interanl ID. This is a protected route, only allowd for current user or admin
        :param user_id: ID of user in the database
        """
        user = get_object_or_404(User, id=user_id)

        return JsonResponse(user.as_dict(), safe=False)

    @method_decorator(require_owner_or_admin)
    def patch(self, request, user_id):
        """
        Do a partial update on a user
        """

        user = get_object_or_404(User, id=user_id)
        try:
            # Grab the project and the updated data
            data = json.loads(request.body)

            # Only update provided fields
            for field, value in data.items():
                if hasattr(user, field):
                    if field == "password":
                        # Passwords need to be hashed
                        user.set_password(value)
                    else:
                        setattr(user, field, value)

            user.save()
            return JsonResponse({"success": f"Partialy updated format {user}"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @method_decorator(require_owner_or_admin)
    def delete(self, request, user_id):
        """Handle DELETE /users/123/"""
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({"success": "User deleted"})
