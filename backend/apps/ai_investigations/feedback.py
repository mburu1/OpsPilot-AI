from django.db import models
from platform.authentication.models import BaseTenantModel
from apps.ai_investigations.models import AIInvestigation

class AIFeedback(BaseTenantModel):
    """
    Stores human feedback on AI-generated hypotheses.
    Used for grounding and future RLHF.
    """
    investigation = models.ForeignKey(
        AIInvestigation,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )
    is_helpful = models.BooleanField()
    correction = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('investigation', 'user')
