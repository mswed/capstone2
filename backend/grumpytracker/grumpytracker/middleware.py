import jwt
from django.conf import settings
from users.models import User
from typing import Any


class JWTAuthMiddleware:
    def __init__(self, get_response) -> None:
        # get_response is used to create middleware
        self.get_response = get_response

    def __call__(self, request) -> Any:
        """
        When the class is called  we check for a JWT in the authorization header
        """
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if auth_header and auth_header.startswith("Bearer "):
            # Grab the toekn
            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
                user = User.objects.get(id=payload.get("user_id"))

                # Set the user as the current user
                request.user = user
            except jwt.ExpiredSignatureError:
                # The token expired
                pass
            except jwt.InvalidTokenError:
                pass
            except User.DoesNotExist:
                pass

        response = self.get_response(request)

        return response
