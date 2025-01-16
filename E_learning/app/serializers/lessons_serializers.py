from rest_framework import serializers

from E_learning.app.models import Lessons


class LessonsSerializer(serializers.ModelSerializer):
    img_url = serializers.ImageField(required=False)
    class Meta:
        model = Lessons
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user
        if user.role != 'LECTURER':
            raise serializers.ValidationError('Only Lecturer create')
        course = data.get('course')
        if course and course.user != user:
            raise serializers.ValidationError("You do not have permission to add lessons to this course.")
        return data
