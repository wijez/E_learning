from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from E_learning.app.models import Enrollments
from E_learning.app.serializers.enrollments_serializers import EnrollmentsSerializer


class EnrollmentsViewSet(viewsets.ModelViewSet):
    queryset = Enrollments.objects.all().order_by('enrolled_at')
    serializer_class = EnrollmentsSerializer
    permission_classes = [permissions.IsAuthenticated]

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
