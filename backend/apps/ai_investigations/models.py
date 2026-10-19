from django.db import models
from platform.authentication.models import BaseTenantModel
from apps.incidents.models import Incident

class AIInvestigation(BaseTenantModel):
    """
    The AI-driven analysis of a specific incident.
    """
    incident = models.OneToOneField(
        Incident,
        on_delete=models.CASCADE,
        related_name='investigation'
    )

    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')],
        default='PENDING'
    )

    # AI Output
    root_cause_hypothesis = models.TextField(blank=True, null=True)
    suggested_remediation = models.TextField(blank=True, null=True)
    confidence_score = models.FloatField(null=True, blank=True)

    # Evidence used by AI
    evidence_links = models.JSONField(default=list, blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Investigation for {self.incident.title}"
