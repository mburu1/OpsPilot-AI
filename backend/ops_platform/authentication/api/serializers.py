from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Add user and primary organization claims to JWT response."""
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        from apps.accounts.membership import OrganizationMember
        membership = OrganizationMember.objects.filter(user=user).first()
        data["user_id"] = str(user.id)
        data["email"] = user.email
        data["organization_id"] = str(membership.organization_id) if membership else None
        data["role"] = membership.role if membership else None
        return data
