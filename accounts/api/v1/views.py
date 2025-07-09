import jwt
from django.core.exceptions import ObjectDoesNotExist
from jwt import ExpiredSignatureError, InvalidSignatureError
from rest_framework.generics import GenericAPIView, UpdateAPIView, RetrieveUpdateAPIView
from .serializers import (
    RegistrationSerializer,
    ProfileSerializer,
    ActivationResendSerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Profile
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
import jwt
from django.conf import settings


from ..utils import EmailThread, get_tokens_for_user_util  # Import the utility function
from accounts.models import UsedToken  # Import the UsedToken model

User = get_user_model()


class RegistrationApiView(GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(
                {
                    "detail": "You are already logged in. Please log out to register a new account."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = get_tokens_for_user_util(user_obj)  # Use utility function

            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                [email],
            )
            EmailThread(email_obj).start()
            # serializer.data.pop('password')
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = get_tokens_for_user_util(user)
        return Response({"token": token, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(UpdateAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # set_password also hashes the password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "Password changed successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class ActivationApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs):
        try:
            token_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token_payload.get("user_id")
            jti = token_payload.get("jti")  # Get JTI from token

            if not user_id or not jti:
                return Response(
                    {"detail": "Token is invalid (missing user_id or jti)."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if this token JTI has been used before
            if UsedToken.objects.filter(token_jti=jti).exists():
                return Response(
                    {"detail": "This activation link has already been used."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has been expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "Token is not valid."}, status=status.HTTP_400_BAD_REQUEST
            )
        except (
            Exception
        ) as e:  # Catch any other potential error during decode or jti access
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = get_object_or_404(User, id=user_id)

        if user_obj.is_verified:
            return Response(
                {"details": "Your account has already been verified."},
                status=status.HTTP_200_OK,
            )

        user_obj.is_verified = True
        user_obj.save()

        # Record the token JTI as used
        UsedToken.objects.create(user=user_obj, token_jti=jti)

        return Response(
            {"details": "Your account has been activated successfully."},
            status=status.HTTP_200_OK,
        )


class ActivationResendApiView(GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = get_tokens_for_user_util(user_obj)  # Use utility function
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@admin.com",
            [user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "User activation resend successfully."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordApiView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(
                {
                    "detail": "You are already logged in. Please log out to reset your password."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        user_obj = get_object_or_404(User, email=email)
        token = get_tokens_for_user_util(user_obj)  # Use utility function

        email_obj = EmailMessage(
            "email/reset_password.tpl", {"token": token}, "admin@admin.com", [email]
        )
        EmailThread(email_obj).start()

        return Response(
            {"details": "Sent reset password email."}, status=status.HTTP_200_OK
        )


class ResetPasswordConfirmApiView(GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, token, *args, **kwargs):
        try:
            token_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token_payload.get("user_id")
            jti = token_payload.get("jti")

            if not user_id or not jti:
                return Response(
                    {"detail": "Token is invalid (missing user_id or jti)."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if this token JTI has been used before
            if UsedToken.objects.filter(token_jti=jti).exists():
                return Response(
                    {"detail": "This password reset link has already been used."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has been expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "Token is not valid."}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:  # Catch any other potential error
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = get_object_or_404(User, id=user_id)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # set_password also hashes the password
        user_obj.set_password(serializer.validated_data.get("new_password"))
        user_obj.save()

        # Record the token JTI as used
        UsedToken.objects.create(user=user_obj, token_jti=jti)

        return Response(
            {"details": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )
