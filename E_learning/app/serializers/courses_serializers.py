from rest_framework import serializers, exceptions

from E_learning.app.models import Courses


class CoursesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        help_text="Tiêu đề của khóa học",
        max_length=500
    )
    description = serializers.CharField(
        help_text="Mô tả chi tiết về khóa học"
    )
    introductor_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        help_text="ID của người tạo khóa học"
    )

    class Meta:
        model = Courses
        fields = "__all__"
        read_only_fields = ['id','introductor_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['introductor_id'] = request.user
            return super().create(validated_data)
        raise exceptions.NotAuthenticated('User must be authenticated')
