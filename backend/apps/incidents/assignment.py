from django.db import models
from platform.authentication.models import BaseTenantModel
from django.conf import settings

class IncidentAssignment(BaseTenantModel):
    """
    Tracks who is currently responsible for an incident.
    """
    incident = models.ForeignKey(
        'incidents.Incident',
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('incident', 'user')
