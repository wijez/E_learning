from rest_framework.permissions import BasePermission


class IsRole(BasePermission):
    """
    Custom permission to allow access based on user roles.
    """

    def __init__(self, allowed_roles):
        """
        Initialize with allowed roles.
        :param allowed_roles: List of roles that are allowed (e.g., [RoleEnum.ADMIN, RoleEnum.LECTURER])
        """
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            # Ensure the user's role is in the allowed roles
            user_role = getattr(request.user, "role", None)
            return user_role in [role.value for role in self.allowed_roles]
        return False
