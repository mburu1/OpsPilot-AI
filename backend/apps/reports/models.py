from django.db import models
from platform.authentication.models import BaseTenantModel
from apps.ai_investigations.models import AIInvestigation

class Report(BaseTenantModel):
    """
    A formalized, structured post-incident report for stakeholders.
    """
    investigation = models.OneToOneField(
        AIInvestigation,
        on_delete=models.CASCADE,
        related_name='report'
    )
    title = models.CharField(max_length=500)
    executive_summary = models.TextField()
    timeline = models.JSONField(default=list) # List of timestamps and events
    final_root_cause = models.TextField()
    preventative_measures = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[('DRAFT', 'Draft'), ('REVIEW', 'In Review'), ('PUBLISHED', 'Published')],
        default='DRAFT'
    )

    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report for {self.investigation.incident.title}"
