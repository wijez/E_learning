from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings

from E_learning.app.models import Users
from E_learning.app.serializers import UsersSerializer, VerifyCodeSerializer
from E_learning.app.serializers.auth_serializers import LoginSerializer, RegisterSerializer
from E_learning.app.serializers.users_serializers import UserTokenSerializer
from E_learning.app.views.base_views import BaseUserViewSet


class RegisterView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={status.HTTP_201_CREATED: UsersSerializer, status.HTTP_400_BAD_REQUEST: 'Validation errors'},
        operation_summary="User Registration",
        operation_description="Register a new user and send a verification email."
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send verification email
            subject = 'Verify your email'
            message = f'Your verification code is: {user.verify_code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return Response({
                'message': 'Registration successful. Please check your email for verification code.',
                'user': UsersSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if not user.is_active:
                return Response({
                    'message': 'Please verify your email first'
                }, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UsersSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=VerifyCodeSerializer,
        responses={status.HTTP_200_OK: 'Email verified successfully', status.HTTP_400_BAD_REQUEST: 'Verify_code error'},
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verify_code = serializer.validated_data['verify_code']

            try:
                user = Users.objects.get(email=email, verify_code=verify_code)
                user.is_active = True
                user.verify_code = ''
                user.save()

                return Response({
                    'message': 'Email verified successfully'
                }, status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                return Response({
                    'message': 'Invalid verification code'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist'),
            },
            required=['refresh']
        ),
        responses={
            status.HTTP_200_OK: openapi.Response('Successfully logged out', examples={
                "application/json": {
                    "message": "Successfully logged out"
                }
            }),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Invalid token or request', examples={
                "application/json": {
                    "detail": "Invalid token or request"
                }
            })
        },
        operation_summary="Logout User",
        operation_description="Blacklists the provided refresh token and logs the user out."
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            print(request.data)
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            blacklisted_tokens = BlacklistedToken.objects.filter(token=token)
            print("Blacklisted Tokens:", blacklisted_tokens)

            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetMeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserTokenSerializer(request.user)
        return Response(serializer.data)
