from rest_framework import viewsets
from .models import AIInvestigation
from .serializers import AIInvestigationSerializer
from platform.permissions.permissions import IsOrganizationMember

class AIInvestigationViewSet(viewsets.ModelViewSet):
    queryset = AIInvestigation.objects.all()
    serializer_class = AIInvestigationSerializer
    permission_classes = [IsOrganizationMember]

    def get_queryset(self):
        user = self.request.user
        from apps.accounts.membership import OrganizationMember
        membership = OrganizationMember.objects.filter(user=user).first()
        return AIInvestigation.objects.filter(organization_id=membership.organization_id if membership else None)
