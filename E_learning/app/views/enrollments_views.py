from rest_framework import permissions, viewsets

from E_learning.app.models import Enrollments
from E_learning.app.serializers.enrollments_serializers import EnrollmentsSerializer


class EnrollmentsViewSet(viewsets.ModelViewSet):
    queryset = Enrollments.objects.all().order_by('enrolled_at')
    serializer_class = EnrollmentsSerializer
    permission_classes = [permissions.IsAuthenticated]


