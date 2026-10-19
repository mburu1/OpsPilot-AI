from django.db import models
from platform.authentication.models import BaseTenantModel
from apps.ai_investigations.models import AIInvestigation

class ChatMessage(BaseTenantModel):
    """
    Stores the conversation history between a user and the AI for a specific investigation.
    """
    investigation = models.ForeignKey(
        AIInvestigation,
        on_delete=models.CASCADE,
        related_name='chat_history'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=10,
        choices=[('user', 'User'), ('assistant', 'AI')],
        default='user'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
