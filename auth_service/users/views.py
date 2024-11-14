# users/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

class RegisterUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
class ValidateTokenView(APIView):
    def post(self, request):
        token_key = request.data.get("token")
        
        if not token_key:
            return Response({"valid": False, "error": "Token missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = Token.objects.get(key=token_key)
            user = token.user  # Access the associated user
            return Response({
                "valid": True,
                "user_id": user.id,
                "username": user.username  # Include username in response
            }, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"valid": False}, status=status.HTTP_401_UNAUTHORIZED)