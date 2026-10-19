from rest_framework import viewsets
from .models import Incident
from .serializers import IncidentSerializer
from platform.permissions.permissions import IsOrganizationMember

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsOrganizationMember]

    def get_queryset(self):
        user = self.request.user
        from apps.accounts.membership import OrganizationMember
        membership = OrganizationMember.objects.filter(user=user).first()
        return Incident.objects.filter(organization_id=membership.organization_id if membership else None)
