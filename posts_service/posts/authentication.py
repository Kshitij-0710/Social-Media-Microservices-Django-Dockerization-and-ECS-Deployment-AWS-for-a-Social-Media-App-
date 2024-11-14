# RemoteTokenAuthentication example in post_project
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
            response = requests.post(
                "http://localhost:8000/api/users/validate-token/",
                json={"token": token},
                timeout=5
            )
            response_data = response.json()

            if response.status_code != 200 or not response_data.get("valid"):
                raise AuthenticationFailed("Invalid token")

            user_id = response_data.get("user_id")
            username = response_data.get("username")

            # Fetch or create the user with user_id and username
            user, _ = User.objects.get_or_create(id=user_id, defaults={'username': username})
            return (user, None)
        except requests.RequestException:
            raise AuthenticationFailed("Authentication service is unavailable")
