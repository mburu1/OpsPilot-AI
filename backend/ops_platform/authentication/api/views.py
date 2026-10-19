from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView
from .serializers import CustomTokenObtainPairSerializer

class TokenObtainPairView(BaseTokenObtainPairView):
    """Obtain JWT access and refresh tokens."""
    serializer_class = CustomTokenObtainPairSerializer

class TokenRefreshView(BaseTokenRefreshView):
    """Refresh a JWT access token."""
