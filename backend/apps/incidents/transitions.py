from django.db import models
from platform.authentication.models import BaseTenantModel

class IncidentStateTransition(BaseTenantModel):
    """
    Audit trail of incident status changes.
    """
    incident = models.ForeignKey(
        'incidents.Incident',
        on_delete=models.CASCADE,
        related_name='transitions'
    )
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
