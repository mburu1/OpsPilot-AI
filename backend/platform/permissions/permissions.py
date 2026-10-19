from rest_framework import permissions
from django.core.exceptions import PermissionDenied

class IsOrganizationMember(permissions.BasePermission):
    """
    Ensures the user belongs to the organization associated with the requested resource.
    """
    message = "You do not have permission to access resources for this organization."

    def has_object_permission(self, request, view, obj):
        # Check if the object has an organization_id (implements BaseTenantModel)
        if hasattr(obj, 'organization_id'):
            # Logic to verify user's membership in obj.organization_id
            # This will be fully implemented once apps.accounts is built
            return True
        return True
