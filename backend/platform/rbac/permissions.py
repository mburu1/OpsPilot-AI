from rest_framework import permissions
from django.core.exceptions import PermissionDenied

class HasRolePermission(permissions.BasePermission):
    """
    Ensures the user has a specific role assigned to them within the organization.
    """
    def has_permission(self, request, view):
        # Required role for the specific view
        required_role = getattr(view, 'required_role', None)
        if not required_role:
            return True

        from platform.rbac.models import UserRole, Role
        try:
            role_obj = Role.objects.get(name=required_role)
            return UserRole.objects.filter(
                user=request.user,
                role=role_obj
            ).exists()
        except Role.DoesNotExist:
            return False
