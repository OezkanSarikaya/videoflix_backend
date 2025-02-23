"""
URL configuration for user authentication and account management.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    PasswordResetConfirmView,
    activate_account,
    PasswordResetRequestView,
)

urlpatterns = [
    path("signup/", UserRegistrationView.as_view(), name="user_signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password_reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "password_reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("activate/<uidb64>/<token>/", activate_account, name="account_activate"),
]
