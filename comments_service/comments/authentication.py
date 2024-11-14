# comment_project/comments/authentication.py
import requests
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class RemoteTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Token "):
            return None

        token = auth_header.split(" ")[1]

        try:
            # Call auth_project's validate-token endpoint to validate the token
            response = requests.post(
                "http://localhost:8000/api/users/validate-token/",
                json={"token": token},
                timeout=5
            )
            response_data = response.json()

            # Check if the token is valid and contains user information
            if response.status_code != 200 or not response_data.get("valid"):
                raise AuthenticationFailed("Invalid token")

            user_id = response_data.get("user_id")
            username = response_data.get("username")

            # Check if a user with the same username exists
            try:
                user = User.objects.get(username=username)
                # If a user with this username exists but has a different ID, use that user as is
                if user.id != user_id:
                    return (user, None)
            except User.DoesNotExist:
                # Create a new user if the username doesn't exist
                user = User(id=user_id, username=username)
                user.save()

            return (user, None)
        except requests.RequestException:
            raise AuthenticationFailed("Authentication service is unavailable")
