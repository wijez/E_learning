from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from rest_framework import permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..contants import RoleEnum
from ..contants.status_enum import ChoicesEnum
from ..security.permission import (
    IsCourseOwnerOrInvitedLecturer,
    IsLecturerPermission,
    IsLecturerAdminOrSuperAdmin)
from ..security.role_permission import IsRole
from ..serializers.courses_serializers import CoursesSerializer, CourseApprovalSerializer
from ..serializers.lessons_serializers import LessonsSerializer
from ..utils.send_mail import send_email_to_admins_and_super_users
from ..views.base_views import BaseUserViewSet
from ..models import Courses


class CoursesViewSet(BaseUserViewSet):
    queryset = Courses.objects.all().order_by('created_at')
    serializer_class = CoursesSerializer
    permission_classes = [IsLecturerAdminOrSuperAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsLecturerPermission()]
        # elif self.action in ['update', 'partial_update', 'destroy']:
        #     return [IsAuthenticated(),IsCourseOwnerOrInvitedLecturer(), IsLecturerAdminOrSuperAdmin()]
        # return super().get_permissions()
        elif self.action in ['approve_course', 'view_course_details', 'list_pending_requests']:
            return [IsAuthenticated(), IsLecturerAdminOrSuperAdmin()]
        return super().get_permissions()

    def filter_queryset(self, queryset):
        user = self.request.user
        if user.role in [RoleEnum.ADMIN.value, RoleEnum.SUPER_USER.value]:
            return queryset
        elif user.role == RoleEnum.LECTURER.value:
            return queryset.filter(models.Q(user=user) | models.Q(invited_lecturers=user))
        else:
            return queryset.filter(is_public=True)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsLecturerPermission])
    def request_approval(self, request, pk=None):
        if request.user.role != RoleEnum.LECTURER.value:
            return Response({"detail": "Only lecturer can request approval"}, status=status.HTTP_403_FORBIDDEN)
        course = self.get_object()
        if course.status in [ChoicesEnum.APPROVED.value.lower(), ChoicesEnum.DRAFT.value.lower()]:
            course.request_approval()
            send_email_to_admins_and_super_users(course=course.title)
            return Response({"detail": "Request for editing submitted successfully."}, status=status.HTTP_200_OK)
        if course.status == ChoicesEnum.PENDING_APPROVAL.value.lower():
            return Response({"detail": "Course must be in draft OR approved status to request approval."},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Approval request submitted successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAuthenticated,IsRole(roles=[RoleEnum.ADMIN.value, RoleEnum.SUPER_USER.value])])
    def approve_course(self, request, pk=None):
        course = self.get_object()
        if course.status != ChoicesEnum.PENDING_APPROVAL.value.lower():
            return Response({"detail": "Course is not in pending approval status."},
                            status=status.HTTP_400_BAD_REQUEST)
        course.approve()
        return Response({"detail": "Course approved and set to public."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsRole(roles=[RoleEnum.ADMIN.value, RoleEnum.SUPER_USER.value])])
    def view_course_details(self, request, pk=None):
        course = self.get_object()
        if course.status not in [ChoicesEnum.PENDING_APPROVAL.value.lower(), ChoicesEnum.APPROVED.value.lower()]:
            return Response({"detail": "Only pending approval courses can be viewed."},
                            status=status.HTTP_400_BAD_REQUEST)

        course_data = CoursesSerializer(course).data
        lessons_data = LessonsSerializer(course.lessons.all(), many=True).data
        return Response({"course": course_data, "lessons": lessons_data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated, IsRole(roles=[RoleEnum.ADMIN.value, RoleEnum.SUPER_USER.value])])
    def list_pending_requests(self, request):
        queryset = Courses.objects.filter(status=ChoicesEnum.PENDING_APPROVAL.value.lower())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for course_data in serializer.data:
                course_instance = queryset.get(pk=course_data['id'])
                lessons_data = LessonsSerializer(course_instance.lessons.all(), many=True).data
                course_data['lessons'] = lessons_data
            return self.get_paginated_response(serializer.data)

