# users/urls.py
from django.urls import path
from .views import RegisterUser, LoginView ,ValidateTokenView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('validate-token/', ValidateTokenView.as_view(), name='validate-token'),
]

