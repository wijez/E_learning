from ..serializers.courses_serializers import CoursesSerializer
from ..views.base_views import BaseUserViewSet
from ..models import Courses
from ..security.admin_permission import IsAdmin


class CoursesViewSet(BaseUserViewSet):
    queryset = Courses.objects.all().order_by('created_at')
    serializer_class = CoursesSerializer
    permission_classes = [IsAdmin]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
