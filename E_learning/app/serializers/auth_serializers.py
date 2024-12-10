from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from E_learning.app.models import Users
from E_learning.app.serializers import UsersSerializer
from E_learning.app.utils.send_mail import send_verification_email


def validate_registration_data(email, username, password):
    # Kiểm tra email đã được đăng ký chưa
    if Users.objects.filter(email=email).exists():
        raise ValidationError({'email': 'This email is already registered.'})

    # Kiểm tra username đã được sử dụng chưa
    if Users.objects.filter(username=username).exists():
        raise ValidationError({'username': 'This username is already taken.'})

    # Kiểm tra độ dài password
    if len(password) < 8:
        raise ValidationError({'password': 'Password must be at least 8 characters long.'})

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
                                        max_length=6,
                                        help_text="Required. The 6-digit verification code sent to your email.")

    def validate(self, attrs):
        email = attrs.get('email')
        verify_code = attrs.get('verify_code')

        try:
            user = Users.objects.get(email=email, verify_code=verify_code)
        except Users.DoesNotExist:
            raise serializers.ValidationError({
                'verify_code': 'Invalid verification code or email.'
            })

        # Update user details after validation
        user.is_active = True
        user.verify_code = ''
        user.save()

        # Add any additional information if needed
        attrs['user'] = user  # Optional: Pass the user instance back if needed
        return attrs

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
        send_verification_email(user.email, user.verify_code)
        return user
    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get('password')
        validate_registration_data(email,username,password)

        return attrs




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Incorrect credentials")
        if not user.is_active:
            raise serializers.ValidationError("Please verify your email first")

        refresh = RefreshToken.for_user(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = UsersSerializer(user).data
        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class PasswordResetVerifiedSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=40)
    password = serializers.CharField(max_length=128)


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)


class EmailChangeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class EmailChangeVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)




