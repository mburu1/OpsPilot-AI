from django.db import models
from platform.authentication.models import BaseTenantModel

class Service(BaseTenantModel):
    """
    Represents a deployable unit of software (e.g., 'auth-api', 'payment-gateway').
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)

    # Status tracking
    STATUS_CHOICES = [
        ('HEALTHY', 'Healthy'),
        ('DEGRADED', 'Degraded'),
        ('DOWN', 'Down'),
        ('MAINTENANCE', 'Maintenance'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='HEALTHY'
    )

    def __str__(self):
        return f"{self.name} ({self.status})"
