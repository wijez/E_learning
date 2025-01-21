from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from E_learning.app.models import Lessons, Courses
from E_learning.app.serializers.lessons_serializers import LessonsSerializer
from E_learning.app.views import BaseUserViewSet


class LessonViewSet(BaseUserViewSet):

    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    parser_classes = (MultiPartParser, FormParser)

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