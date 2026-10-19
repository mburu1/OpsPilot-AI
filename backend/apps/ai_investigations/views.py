from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AIInvestigation
from .feedback import AIFeedback
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

    @action(detail=True, methods=['post'])
    def provide_feedback(self, request, pk=None):
        """
        Endpoint to submit human feedback on an AI investigation.
        """
        investigation = self.get_object()
        is_helpful = request.data.get('is_helpful')
        correction = request.data.get('correction', '')

        if is_helpful is None:
            return Response({"error": "is_helpful is required"}, status=status.HTTP_400_BAD_REQUEST)

        feedback, created = AIFeedback.objects.update_or_create(
            investigation=investigation,
            user=request.user,
            defaults={'is_helpful': is_helpful, 'correction': correction}
        )

        return Response({"status": "feedback recorded"})
