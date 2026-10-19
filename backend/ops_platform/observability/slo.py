from django.db import models
from ops_platform.authentication.models import BaseTenantModel

class SLODefinition(BaseTenantModel):
    """Service Level Objective definition."""
    service_name = models.CharField(max_length=255)
    metric_name = models.CharField(max_length=255)
    target_value = models.FloatField()
    threshold_window_minutes = models.IntegerField(default=60)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service_name} - {self.metric_name} ({self.target_value})"

class SLOViolation(BaseTenantModel):
    """Recorded SLO violation."""
    slo = models.ForeignKey(SLODefinition, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    actual_value = models.FloatField()
    status = models.CharField(
        max_length=20, choices=[("ACTIVE", "Active"), ("RESOLVED", "Resolved")], default="ACTIVE"
    )

    def __str__(self):
        return f"Violation of {self.slo.service_name} at {self.start_time}"
