from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from E_learning.app.models import Users
from E_learning.app.serializers.users_serializers import UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('created_at')
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]
