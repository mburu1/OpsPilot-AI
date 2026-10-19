from django.db import models
from platform.authentication.models import BaseTenantModel
from apps.events.models import Event

class CorrelationRule(BaseTenantModel):
    """
    Defines a rule for grouping events into an incident.
    Example: "If 5 ERROR events from the same service occur within 1 minute"
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Logic definition (Simplified for now: stored as a JSON configuration)
    # In production, this could be a DSL or Python expression
    logic_config = models.JSONField(default=dict)

    is_active = models.BooleanField(default=True)
    priority_override = models.CharField(
        max_length=20,
        choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
