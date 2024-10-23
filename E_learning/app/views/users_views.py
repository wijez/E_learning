from rest_framework import permissions, viewsets

from E_learning.app.models import Users
from E_learning.app.serializers.users_serializers import UsersSerializer
from ..security.admin_permission import IsAdmin


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('created_at')
    serializer_class = UsersSerializer
    permission_classes = [IsAdmin]
