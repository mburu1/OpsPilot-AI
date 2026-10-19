from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer

class TokenObtainPairView(TokenObtainPairView):
    """
    Endpoint to obtain Access and Refresh tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer

class TokenRefreshView(TokenRefreshView):
    """
    Endpoint to refresh the Access token using a Refresh token.
    """
    pass
