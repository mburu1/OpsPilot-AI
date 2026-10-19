from django.db import models
from platform.authentication.models import BaseTenantModel

class NotificationChannel(BaseTenantModel):
    """
    Stores configuration for external notification channels (Slack/Teams).
    """
    name = models.CharField(max_length=100)
    provider_type = models.CharField(
        max_length=20,
        choices=[('slack', 'Slack'), ('teams', 'Microsoft Teams')],
        default='slack'
    )
    config = models.JSONField(default=dict) # Stores webhook_url, etc.
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.provider_type})"
