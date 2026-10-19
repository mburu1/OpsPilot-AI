from django.db import models
from django.conf import settings

class Permission(models.Model):
    """
    Fine-grained permission definitions.
    Example: 'incident.view', 'report.publish'
    """
    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code

class Role(models.Model):
    """
    Groups of permissions.
    """
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    """
    Links users to roles within an organization.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    organization_id = models.UUIDField(db_index=True)

    class Meta:
        unique_together = ('user', 'role', 'organization_id')
