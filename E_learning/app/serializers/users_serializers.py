from ..models.users_models import Users
from rest_framework import serializers


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'image', 'email', 'password', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
