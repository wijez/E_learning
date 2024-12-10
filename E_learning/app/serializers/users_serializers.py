from rest_framework import serializers
from ..models.users_models import Users


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'verify_code', 'name', 'email', 'password', 'role']
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



class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'email', 'name', 'username', 'image', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'username', 'image']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance