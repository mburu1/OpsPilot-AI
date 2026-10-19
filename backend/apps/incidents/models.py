from django.db import models
from platform.authentication.models import BaseTenantModel
from apps.events.models import Event

class Incident(BaseTenantModel):
    """
    A correlated group of events representing a system failure or anomaly.
    """
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[('OPEN', 'Open'), ('INVESTIGATING', 'Investigating'), ('RESOLVED', 'Resolved'), ('CLOSED', 'Closed')],
        default='OPEN'
    )

    priority = models.CharField(
        max_length=20,
        choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')],
        default='MEDIUM'
    )

    # Relation to events that triggered this incident
    events = models.ManyToManyField(Event, related_name='incidents')

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.priority}] {self.title}"
