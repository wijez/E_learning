from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError
from E_learning.app.models import Users


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     style={'input_type': 'password'},
                                     help_text="Required. Your password must be at least 8 characters long.")
    password_confirm = serializers.CharField(write_only=True, required=True,
                                             style={'input_type': 'password'},
                                             help_text="Required. Must match password field.")
    email = serializers.EmailField(required=True,
                                   help_text="Required. Enter a valid email address.")
    name = serializers.CharField(required=True,
                                 help_text="Required. Your full name.")
    username = serializers.CharField(required=True,
                                     help_text="Required. Choose a unique username.")

    class Meta:
        model = Users
        fields = ('email', 'name', 'password', 'password_confirm', 'username')

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({
                "password_confirm": "Password confirmation does not match."
            })
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        try:
            user = Users.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                name=validated_data['name'],
                password=validated_data['password']
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,
                                   help_text="Required. Your registered email address.")
    password = serializers.CharField(required=True,
                                     style={'input_type': 'password'},
                                     help_text="Required. Your password.")


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,
                                   help_text="Required. The email address you registered with.")
    verify_code = serializers.CharField(required=True,
                                        help_text="Required. The 6-digit verification code sent to your email.")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'name', 'password', 'username']

    def create(self, validated_data):
        user = Users(
            email=validated_data['email'],
            name=validated_data['name'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


