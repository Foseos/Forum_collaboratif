from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (ConfirmEmailView, RegisterView, RequestEmailChangeView,
                    ResendConfirmationView, TrackedTokenObtainPairView,
                    PasswordResetRequestView, PasswordResetConfirmView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", TrackedTokenObtainPairView.as_view(), name="auth-login"),
    path("refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("confirm-email/", ConfirmEmailView.as_view(), name="auth-confirm-email"),
    path("resend-confirmation/", ResendConfirmationView.as_view(), name="auth-resend-confirmation"),
    path("request-email-change/", RequestEmailChangeView.as_view(), name="auth-request-email-change"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="auth-password-reset"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="auth-password-reset-confirm"),
]
