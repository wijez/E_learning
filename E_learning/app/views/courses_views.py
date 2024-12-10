from rest_framework import permissions, exceptions
from ..contants import RoleEnum
from ..serializers.courses_serializers import CoursesSerializer
from ..views.base_views import BaseUserViewSet
from ..models import Courses


class CoursesViewSet(BaseUserViewSet):
    queryset = Courses.objects.all().order_by('created_at')
    serializer_class = CoursesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Lọc danh sách khóa học dựa trên vai trò của người dùng.
        """
        user = self.request.user
        role = getattr(user, 'role', None)

        if role == RoleEnum.ADMIN.value:
            return Courses.objects.all().order_by('created_at')
        elif role == RoleEnum.LECTURER.value:
            return Courses.objects.filter(user_id=user.id).order_by('created_at')
        elif role == RoleEnum.USER.value:
            return Courses.objects.filter(is_public=True).order_by('created_at')  # Chỉ lấy các khóa học công khai
        return Courses.objects.none()

    def perform_create(self, serializer):
        """
        Kiểm tra quyền và tạo khóa học.
        """
        user = self.request.user
        role = getattr(user, 'role', None)
        if role not in [RoleEnum.ADMIN.value, RoleEnum.LECTURER.value]:
            raise exceptions.PermissionDenied("You do not have permission to create a course.")
        serializer.save(user_id=user.id)

    def perform_update(self, serializer):
        """
        Kiểm tra quyền và cập nhật khóa học.
        """
        user = self.request.user
        role = getattr(user, 'role', None)
        if role not in [RoleEnum.ADMIN.value, RoleEnum.LECTURER.value]:
            raise exceptions.PermissionDenied("You do not have permission to update this course.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Kiểm tra quyền và xóa khóa học.
        """
        user = self.request.user
        role = getattr(user, 'role', None)
        if role != RoleEnum.ADMIN.value:
            raise exceptions.PermissionDenied("Only ADMIN can delete courses.")
        return super().destroy(request, *args, **kwargs)
