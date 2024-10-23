from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users with the 'ADMIN' role to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            # Check if the user role is ADMIN
            return request.user.role == 'ADMIN'
        return False
