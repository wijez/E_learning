from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from E_learning.app.models import Lessons, Courses
from E_learning.app.serializers.lessons_serializers import LessonsSerializer
from E_learning.app.views import BaseUserViewSet


class LessonViewSet(BaseUserViewSet):

    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    @swagger_auto_schema(
        request_body=LessonsSerializer,
        responses={status.HTTP_200_OK: openapi.Response('Verification code sent to email.'),
                   status.HTTP_400_BAD_REQUEST: 'Validation errors'}
    )
    def filter_queryset(self, queryset):
        queryset = queryset.filter(course__user=self.request.user).order_by('created_at')
        return queryset

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        user = request.user

        # Kiểm tra xem user có sở hữu course không
        if not Courses.objects.filter(id=course_id, user=user).exists():
            return Response({"detail": "You do not have permission to add lessons to this course."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)