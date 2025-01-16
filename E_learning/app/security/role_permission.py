from rest_framework.permissions import BasePermission


class IsRole(BasePermission):
    """
    Custom permission to allow access based on user roles.
    """
    def __init__(self, roles):
        self.roles = roles
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in self.roles
