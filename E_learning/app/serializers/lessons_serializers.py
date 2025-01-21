
import cloudinary.uploader
from rest_framework import serializers

from E_learning.app.models import Lessons


class LessonsSerializer(serializers.ModelSerializer):
    img_file = serializers.ImageField(write_only=True, required=False)
    video_file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Lessons
        fields = '__all__'
        read_only_fields = ['video_url', 'img_url', 'created_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user
        if user.role != 'LECTURER':
            raise serializers.ValidationError('Only Lecturer create')
        course = data.get('course')
        if course and course.user != user:
            raise serializers.ValidationError("You do not have permission to add lessons to this course.")
        return data

    def create(self, validated_data):
        img = validated_data.pop('img_file', None)
        video = validated_data.pop('video_file', None)

        # Upload image to Cloudinary
        if img:
            img_upload = cloudinary.uploader.upload(img, resource_type="image")
            validated_data['img_url'] = img_upload.get('url')

        # Upload video to Cloudinary
        if video:
            video_upload = cloudinary.uploader.upload(video, resource_type="video")
            validated_data['video_url'] = video_upload.get('url')

        return super().create(validated_data)

