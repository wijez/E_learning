from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from E_learning.app.contants import RoleEnum


class IsLecturerAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and getattr(user, 'role', None) in [
            RoleEnum.LECTURER, RoleEnum.ADMIN, RoleEnum.SUPER_USER
        ]

class IsCourseOwnerOrInvitedLecturer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.course.user == user or user in obj.course.invited_lecturers.all()


class IsLecturerPermission(permissions.BasePermission):
    """
    Custom permission to only allow users with the role 'LECTURER' to create courses.
    """
    def has_permission(self, request, view):
        if view.action == 'create' and request.user.role != 'LECTURER':
            raise PermissionDenied('Only lecturers can create courses.')
        return True


class CustomUserCreationPermission(permissions.BasePermission):
    """
    Custom permission to allow:
    - ADMIN to create, update, delete users and lecturers.
    - SUPER_USER to create, update, delete admins, users, and lecturers.
    - LECTURER to view, add, and delete users registered in their courses.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        target_role = request.data.get('role')
        if request.user.is_superuser:
            # SUPER_USER can manage all roles
            return target_role in ['ADMIN', 'USER', 'LECTURER']
        elif request.user.role == 'ADMIN':
            # ADMIN can manage users and lecturers
            return target_role in ['USER', 'LECTURER']
        elif request.user.role == 'LECTURER':
            # LECTURER can only manage their own students
            if view.action in ['create', 'destroy']:
                # Ensure that they are managing users registered in their courses
                return target_role == 'USER' and 'course_id' in request.data
            elif view.action == 'list':
                return True
        return False

    def has_object_permission(self, request, view, obj):
        # LECTURER can only manage users registered in their courses
        if request.user.role == 'LECTURER':
            return obj.courses.filter(lecturers=request.user).exists()
        return True

class AdminPermissions(permissions.BasePermission):
    """
    Permission for Admin: Can manage users and lecturers.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class SuperUserPermissions(permissions.BasePermission):
    """
    Permission for Super User: Can manage admins, users, and lecturers.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class LecturerPermissions(permissions.BasePermission):
    """
    Permission for Lecturer: Can only manage users registered to their courses.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'LECTURER':
            if view.action in ['list', 'retrieve']:
                return True
            if view.action in ['create', 'destroy']:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        # Ensure the lecturer can only manage users registered to their courses
        return request.user.role == 'LECTURER' and obj.courses.filter(lecturers=request.user).exists()
