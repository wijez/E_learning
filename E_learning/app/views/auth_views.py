from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from E_learning.app.serializers import UsersSerializer, VerifyCodeSerializer
from E_learning.app.serializers.auth_serializers import LoginSerializer, RegisterSerializer, PasswordResetSerializer, \
    PasswordResetVerifiedSerializer
from E_learning.app.serializers.users_serializers import UserTokenSerializer



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
            return Response({
                'message': 'Registration successful. Please check your email for verification code.',
                'user': UsersSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
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
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
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
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Parse and blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({"detail": f"Invalid or expired token `{e}`."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetMeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserTokenSerializer(request.user)
        return Response(serializer.data)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=PasswordResetSerializer,  # Ensure the serializer is passed to request_body
        responses={status.HTTP_200_OK: openapi.Response('Verification code sent to email.'),
                   status.HTTP_400_BAD_REQUEST: 'Validation errors'}
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Verification code sent to email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordVerifyView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=PasswordResetVerifiedSerializer,
        responses={status.HTTP_200_OK: 'Email verified successfully',
                   status.HTTP_400_BAD_REQUEST: 'Verify_code error'}
    )
    def post(self, request):
        serializer = PasswordResetVerifiedSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



