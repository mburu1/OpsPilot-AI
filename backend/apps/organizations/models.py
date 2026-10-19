from django.db import models

from ops_platform.authentication.models import BaseTenantModel


class Organization(BaseTenantModel):
    """The top-level entity for multi-tenancy."""

    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)

    # The root organization has no parent organization.
    organization_id = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return self.name
