from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Incident
from .assignment import IncidentAssignment
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

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Assign the incident to a user.
        """
        incident = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        IncidentAssignment.objects.create(
            incident=incident,
            user_id=user_id,
            is_primary=request.data.get('is_primary', False)
        )

        return Response({"status": "assigned successfully"})

    @action(detail=True, methods=['post'])
    def transition(self, request, pk=None):
        """
        Update incident status with a mandatory comment.
        """
        incident = self.get_object()
        new_status = request.data.get('status')
        comment = request.data.get('comment', '')

        if not new_status:
            return Response({"error": "status is required"}, status=status.HTTP_400_BAD_REQUEST)

        incident.transition_to(new_status, request.user, comment)

        return Response({"status": f"transitioned to {new_status}"})
