from rest_framework.exceptions import PermissionDenied

from ..models.enrollments_models import Enrollments
from rest_framework import serializers, exceptions


class EnrollmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollments
        fields = "__all__"
        read_only_fields = ['id', 'user_id', 'enrolled_at', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user_id'] = request.user
            return super().create(validated_data)
        raise exceptions.NotAuthenticated('User must be authenticated')

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Enrollments.objects.none()

        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("User must be authenticated")

        if user.role == "ADMIN":
            return Enrollments.objects.all().order_by('enrolled_at')

        if user.role == "USER":
            return Enrollments.objects.filter(user_id=user.id).order_by('enrolled_at')

        raise PermissionDenied('You do not have permission to perform this action.')