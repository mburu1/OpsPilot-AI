from rest_framework import viewsets
from .models import KnowledgeArticle
from .serializers import KnowledgeArticleSerializer
from platform.permissions.permissions import IsOrganizationMember

class KnowledgeArticleViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeArticle.objects.all()
    serializer_class = KnowledgeArticleSerializer
    permission_classes = [IsOrganizationMember]

    def get_queryset(self):
        user = self.request.user
        from apps.accounts.membership import OrganizationMember
        membership = OrganizationMember.objects.filter(user=user).first()
        return KnowledgeArticle.objects.filter(organization_id=membership.organization_id if membership else None)
