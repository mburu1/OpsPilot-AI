from django.db import models
import uuid

class BaseTenantModel(models.Model):
    """
    Abstract base class for all tenant-aware models.
    Ensures that every record is linked to an organization for strict isolation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True) # Linked via ID to avoid circular imports in base
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
