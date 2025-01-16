from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template.context_processors import request
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, status, permissions, serializers


from ..contants import RoleEnum
from ..security.permission import (
    IsCourseOwnerOrInvitedLecturer,
    IsLecturerPermission,
    IsLecturerAdminOrSuperAdmin)
from ..serializers.courses_serializers import CoursesSerializer
from ..views.base_views import BaseUserViewSet
from ..models import Courses


class CoursesViewSet(BaseUserViewSet):
    queryset = Courses.objects.all().order_by('created_at')
    serializer_class = CoursesSerializer
    permission_classes = [IsLecturerAdminOrSuperAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated(), IsLecturerPermission()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsCourseOwnerOrInvitedLecturer(), IsLecturerAdminOrSuperAdmin()]
        return super().get_permissions()

    def filter_queryset(self, queryset):
        user = self.request.user

        if user.role in [RoleEnum.ADMIN.value, RoleEnum.SUPER_USER.value]:
            return Courses.objects.all()

        if user.role == RoleEnum.LECTURER.value:
            return Courses.objects.filter(models.Q(user=user) | models.Q(invited_lecturers=user))

        return Courses.objects.filter(is_public=True)

