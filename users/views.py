"""
Views for user authentication and account management.
"""

import os
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.http import JsonResponse, HttpResponse
from django.conf import settings
# from django.db import IntegrityError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .serializers import UserRegistrationSerializer

User = get_user_model()
FRONTEND_URL = os.getenv("FRONTEND_URL", "").rstrip("/")  # Sicherstellen, dass kein doppelter `/` entsteht


def activate_account(request, uidb64, token):
    """
    Activates a user account if the provided token is valid.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Invalid link", status=400)

    if not default_token_generator.check_token(user, token):
        return HttpResponse("Invalid token", status=400)

    user.is_active = True
    user.save()
    return JsonResponse({"message": "Account successfully activated!"})


class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account successfully created."}, status=status.HTTP_201_CREATED)

        if User.objects.filter(email=request.data.get("email")).exists():
            return Response({"detail": "Email already registered."}, status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    """
    API endpoint to request a password reset.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "No user found with this email address."}, status=status.HTTP_400_BAD_REQUEST)

        uid = urlsafe_base64_encode(str(user.pk).encode())
        token = default_token_generator.make_token(user)
        reset_link = f"{FRONTEND_URL}/reset-password/{uid}/{token}/"

        subject = "Password Reset Request"
        html_message = render_to_string("password_reset_email.html", {"user": user, "reset_link": reset_link})
        plain_message = strip_tags(html_message)

        email_msg = EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email_msg.attach_alternative(html_message, "text/html")
        email_msg.send()

        return Response({"message": "Password reset link has been sent!"}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    API endpoint to confirm password reset using a token.
    """
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        """
        Validates the reset token and returns a response.
        """
        user = self._get_user(uidb64)
        if not user or not default_token_generator.check_token(user, token):
            return Response({"detail": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Token is valid."}, status=status.HTTP_200_OK)

    def post(self, request, uidb64, token):
        """
        Resets the user's password if the token is valid.
        """
        user = self._get_user(uidb64)
        if not user or not default_token_generator.check_token(user, token):
            return Response({"detail": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

        form = SetPasswordForm(user, data=request.data)
        if form.is_valid():
            form.save()
            return Response({"detail": "Password successfully reset."}, status=status.HTTP_200_OK)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_user(self, uidb64):
        """
        Helper method to get a user object from a UID.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None
