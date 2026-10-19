from django.db import models
from django.conf import settings
from platform.authentication.models import BaseTenantModel

class OrganizationMember(BaseTenantModel):
    """
    Links users to organizations with specific roles.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='members'
    )
    role = models.CharField(
        max_length=50,
        choices=[('admin', 'Admin'), ('editor', 'Editor'), ('viewer', 'Viewer')],
        default='viewer'
    )

    class Meta:
        unique_together = ('user', 'organization')
