from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer
from platform.permissions.permissions import IsOrganizationMember

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizationMember]

    def get_queryset(self):
        # Enforce tenant isolation
        user = self.request.user
        return Event.objects.filter(organization_id=self.get_organization_id(user))

    def get_organization_id(self, user):
        from apps.accounts.membership import OrganizationMember
        membership = OrganizationMember.objects.filter(user=user).first()
        return membership.organization_id if membership else None
