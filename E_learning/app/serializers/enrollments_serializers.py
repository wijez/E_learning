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