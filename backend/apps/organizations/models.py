from django.db import models
from platform.authentication.models import BaseTenantModel

class Organization(BaseTenantModel):
    """
    The top-level entity for multi-tenancy.
    """
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # We override organization_id for the root organization object itself
    organization_id = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return self.name
