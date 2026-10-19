from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes the JWT payload to include user-specific and tenant-specific data.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom claims to the JWT token
        user = self.user
        # Fetch the primary organization for the user to simplify frontend requests
        from apps.accounts.membership import OrganizationMember
        membership = OrganizationMember.objects.filter(user=user).first()

        data['user_id'] = user.id
        data['email'] = user.email
        data['organization_id'] = membership.organization_id if membership else None
        data['role'] = membership.role if membership else None

        return data
