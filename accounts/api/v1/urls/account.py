from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .. import views

urlpatterns = [
    # Registration
    path("registration/", views.RegistrationApiView.as_view(), name="registration"),
    # Activation
    path(
        "activation/confirm/<str:token>",
        views.ActivationApiView.as_view(),
        name="activation",
    ),
    # Resend Activation
    path(
        "activation/resend/",
        views.ActivationResendApiView.as_view(),
        name="activation_resend",
    ),
    # Change Password
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # Reset Password
    path(
        "reset-password/", views.ResetPasswordApiView.as_view(), name="reset-password"
    ),
    path(
        "reset-password-confirm/<str:token>",
        views.ResetPasswordConfirmApiView.as_view(),
        name="reset-password-confirm",
    ),
    # Login - Token
    path("token/login", views.CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    # Login - JWT
    path("jwt/token/", views.CustomTokenObtainPairView.as_view(), name="token-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token-verify"),
]
