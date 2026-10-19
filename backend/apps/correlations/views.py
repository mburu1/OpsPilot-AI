from rest_framework import viewsets
from .models import CorrelationRule
from .serializers import CorrelationRuleSerializer
from platform.permissions.permissions import IsOrganizationMember

class CorrelationRuleViewSet(viewsets.ModelViewSet):
    queryset = CorrelationRule.objects.all()
    serializer_class = CorrelationRuleSerializer
    permission_classes = [IsOrganizationMember]

    def get_queryset(self):
        user = self.request.user
        from apps.accounts.membership import OrganizationMember
        membership = OrganizationMember.objects.filter(user=user).first()
        return CorrelationRule.objects.filter(organization_id=membership.organization_id if membership else None)
