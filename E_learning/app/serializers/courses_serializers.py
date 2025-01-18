from Tools.scripts.md5sum import usage
from django.template.context_processors import request
from rest_framework import serializers, exceptions

from E_learning.app.contants import RoleEnum
from E_learning.app.contants.status_enum import ChoicesEnum
from E_learning.app.models import Courses, Lessons, Users


class CoursesSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Courses
        fields = "__all__"
        read_only_fields = ['id','user', 'created_at', 'updated_at', 'is_public', 'status']

    def create(self, validated_data):
        user = self.context['request'].user
        if user.role == RoleEnum.LECTURER.value:
            validated_data['is_public'] = False
            validated_data['status'] = ChoicesEnum.DRAFT.value.lower()
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if instance.status == ChoicesEnum.APPROVED.value.lower() and user.role == RoleEnum.LECTURER.value:
            raise serializers.ValidationError("Lecturers cannot update an approved course.")

        if 'is_public' in validated_data and validated_data['is_public']:
            if user.role not in [RoleEnum.ADMIN.value, RoleEnum.SUPER_USER.value]:
                raise serializers.ValidationError("Only admin or superuser can approve the course to be public.")

        if 'status' in validated_data:
            new_status = validated_data['status']
            if new_status == ChoicesEnum.PENDING_APPROVAL.value.lower():
                if user.role != RoleEnum.LECTURER.value:
                    raise serializers.ValidationError("Only lecturers can request approval.")
            elif new_status == ChoicesEnum.APPROVED.value.lower():
                if user.role not in [RoleEnum.ADMIN.value, RoleEnum.SUPER_USER.value]:
                    raise serializers.ValidationError("Only admin or superuser can approve the course.")
                validated_data['is_public'] = True
            elif new_status == ChoicesEnum.PENDING_APPROVAL.value.lower():
                if user.role not in [RoleEnum.ADMIN.value, RoleEnum.SUPER_USER.value]:
                    raise serializers.ValidationError("Only admin or superuser can set course back to pending approval.")
                validated_data['is_public'] = False

        return super().update(instance, validated_data)


class CourseApprovalSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()