from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions, viewsets

from E_learning.app.models import Users, Enrollments
from E_learning.app.serializers.users_serializers import UsersSerializer
from ..contants import RoleEnum
from ..security.permission import CustomUserCreationPermission
from ..security.role_permission import IsRole


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('created_at')
    serializer_class = UsersSerializer
    permission_classes = [CustomUserCreationPermission, permissions.IsAuthenticated]

    def get_permissions(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return [permissions.IsAuthenticated()]

        if self.action in ['create']:
            if user.is_superuser:
                print("superuser", user.is_superuser)
                return [permissions.IsAuthenticated(), IsRole(RoleEnum.SUPER_USER.value)]
            elif user.role == RoleEnum.ADMIN.value:
                return [permissions.IsAuthenticated(), IsRole(RoleEnum.ADMIN.value)]
            else:
                return [permissions.IsAuthenticated()]

        if self.action in ['update', 'partial_update', 'destroy']:
            if user.is_superuser:
                return [permissions.IsAuthenticated(), IsRole(RoleEnum.SUPER_USER.value)]
            elif user.role == RoleEnum.ADMIN.value:
                return [permissions.IsAuthenticated(), IsRole(RoleEnum.ADMIN.value)]
            elif user.role == RoleEnum.LECTURER.value:
                return [permissions.IsAuthenticated(), IsRole(RoleEnum.LECTURER.value)]

        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        # Kiểm tra nếu người dùng là AnonymousUser
        if isinstance(user, AnonymousUser):
            return Users.objects.none()
        queryset = super().get_queryset()
        print(queryset)
        # người dùng đăng kí khóa học thuộc sở hữu của giảng viên
        if user.role == RoleEnum.LECTURER.value:
            queryset = queryset.filter(
                id__in=Enrollments.objects.filter(course_id__user=user).values_list('user_id', flat=True)
            ).distinct()
        elif user.role == RoleEnum.ADMIN.value:
            queryset = queryset.filter(role__in=[RoleEnum.USER.value, RoleEnum.LECTURER.value])
        return queryset

