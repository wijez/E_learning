from Tools.scripts.md5sum import usage
from django.template.context_processors import request
from rest_framework import serializers, exceptions

from E_learning.app.models import Courses, Lessons, Users


class CoursesSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Courses
        fields = "__all__"
        read_only_fields = ['id','user', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)