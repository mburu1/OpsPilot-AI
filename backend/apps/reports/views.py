from rest_framework import viewsets
from .models import Report
from .serializers import ReportSerializer
from platform.permissions.permissions import IsOrganizationMember

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsOrganizationMember]

    def get_queryset(self):
        user = self.request.user
        from apps.accounts.membership import OrganizationMember
        membership = OrganizationMember.objects.filter(user=user).first()
        return Report.objects.filter(organization_id=membership.organization_id if membership else None)
