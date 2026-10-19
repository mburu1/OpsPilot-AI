from django.db import models
from platform.authentication.models import BaseTenantModel
from apps.services.models import Service

class Event(BaseTenantModel):
    """
    Raw operational events (logs, metrics, traces) emitted by services.
    """
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='events'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    LEVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='INFO')

    message = models.TextField()

    # JSONField for flexible metadata (trace IDs, pod names, etc.)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.level}] {self.service.name}: {self.message[:50]}..."
