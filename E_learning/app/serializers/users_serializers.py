from rest_framework import serializers
from ..models.users_models import Users


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Users(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username','email', 'role']
