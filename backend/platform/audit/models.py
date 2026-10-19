from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    """
    Immutable record of all critical system actions.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255) # e.g., 'PUBLISH_REPORT'
    entity_type = models.CharField(max_length=100) # e.g., 'Report'
    entity_id = models.CharField(max_length=255)
    changes = models.JSONField(default=dict) # { 'old': ..., 'new': ... }
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    organization_id = models.UUIDField(db_index=True)

    class Meta:
        ordering = ['-timestamp']
