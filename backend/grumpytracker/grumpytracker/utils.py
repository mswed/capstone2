from typing import Dict, List, Any, Optional
from functools import wraps
from users.models import User

from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def validate_required_fields(
    data: Dict[str, Any], required_fields: List
) -> Optional[str]:
    """
    A utility to make sure we have the needed fields
    """
    for field in required_fields:
        if not data.get(field):
            return f"{field} is required"

    return None


def login_required(view):
    """
    Middleware to make sure the user is logged in
    """

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login required"}, status=401)
        return view(request, *args, **kwargs)

    return wrapper


def require_owner_or_admin(view):
    """
    Middleware to make sure the user can only edit their own records
    or an admin that can edit all
    """

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # First authenticate
            return JsonResponse({"error": "Login required"}, status=401)

        user_id = kwargs.get("user_id")
        if not user_id:
            # Make sure we passed a user_id
            return JsonResponse({"error": "Route requires a user_id"}, status=401)

        owner = get_object_or_404(User, id=user_id)
        if request.user != owner and not request.user.is_superuser:
            # The user is not allowed to access this route
            return JsonResponse({"error": "Permission denied!"}, status=403)

        return view(request, *args, **kwargs)

    return wrapper


def require_admin(view):
    """
    Middleware to make sure the an admin can access the route
    """

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # First authenticate
            return JsonResponse({"error": "Login required"}, status=401)

        if not request.user.is_superuser:
            # The user is not allowed to access this route
            return JsonResponse({"error": "Permission denied!"}, status=403)

        return view(request, *args, **kwargs)

    return wrapper
