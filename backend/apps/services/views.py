from rest_framework import viewsets
from .models import Service
from .serializers import ServiceSerializer
from platform.permissions.permissions import IsOrganizationMember

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsOrganizationMember]

    def get_queryset(self):
        # Enforce tenant isolation
        user = self.request.user
        return Service.objects.filter(organization_id=self.get_organization_id(user))

    def get_organization_id(self, user):
        # This helper would typically fetch the active org from request/session
        # For now, it returns the first org the user belongs to
        from apps.accounts.membership import OrganizationMember
        membership = OrganizationMember.objects.filter(user=user).first()
        return membership.organization_id if membership else None
