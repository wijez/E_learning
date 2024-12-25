from rest_framework import serializers, exceptions

from E_learning.app.contants import RoleEnum
from E_learning.app.models import Courses


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"
        read_only_fields = ['id','user_id', 'created_at', 'updated_at']

    def check_permission(self, role, action):
        """
        Kiểm tra quyền của người dùng dựa trên vai trò và hành động.
        """
        if action == 'create' and role not in [RoleEnum.ADMIN.value, RoleEnum.LECTURER.value]:
            raise exceptions.PermissionDenied("You do not have permission to create a course.")
        elif action == 'update' and role not in [RoleEnum.ADMIN.value, RoleEnum.LECTURER.value]:
            raise exceptions.PermissionDenied("You do not have permission to update this course.")

    def validate(self, attrs):
        """
        Kiểm tra quyền dựa trên vai trò người dùng.
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise exceptions.NotAuthenticated("User must be authenticated.")

        user = request.user
        role = getattr(user, 'role', None)

        if self.instance:  # Update action
            self.check_permission(role, 'update')
        else:  # Create action
            self.check_permission(role, 'create')

        return super().validate(attrs)

    def to_representation(self, instance):
        """
        Chỉ cho phép người dùng có quyền xem khóa học công khai.
        """
        request = self.context.get('request')
        user = request.user
        role = getattr(user, 'role', None)

        if role == RoleEnum.USER.value and not instance.is_public:
            raise exceptions.PermissionDenied("You do not have permission to view this course.")

        return super().to_representation(instance)

    def create(self, validated_data):
        """
        Kiểm tra quyền và tạo khóa học.
        """
        request = self.context.get('request')
        user = request.user
        role = getattr(user, 'role', None)
        self.check_permission(role, 'create')

        validated_data['user_id'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Kiểm tra quyền và cập nhật khóa học.
        """
        request = self.context.get('request')
        user = request.user
        role = getattr(user, 'role', None)
        self.check_permission(role, 'update')

        return super().update(instance, validated_data)