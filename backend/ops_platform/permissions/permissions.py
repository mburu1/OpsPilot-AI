from rest_framework import permissions

class IsOrganizationMember(permissions.BasePermission):
    """Permission hook for tenant-scoped objects."""
    message = "You do not have permission to access resources for this organization."

    def has_object_permission(self, request, view, obj):
        # Tenant membership checks must be implemented against the application's
        # membership model before enabling this permission in production.
        return hasattr(obj, "organization_id")
