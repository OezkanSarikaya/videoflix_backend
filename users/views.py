from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.db import IntegrityError
from dotenv import load_dotenv
from pathlib import Path
import os

from .serializers import UserRegistrationSerializer  # Re-added missing import

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

FRONTEND_URL = os.getenv("FRONTEND_URL")
User = get_user_model()


def activate_account(request, uidb64, token):
    """
    Activate a user account if the provided token is valid.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return JsonResponse({"message": "Account successfully activated!"})
        return HttpResponse("Invalid token", status=400)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Invalid link", status=400)


class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Account successfully created."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"detail": "Email already registered."}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        reset_link = f"{FRONTEND_URL}reset-password/{uid}/{token}/"

        subject = "Password Reset Request"
        html_message = render_to_string("password_reset_email.html", {"user": user, "reset_link": reset_link})
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email.attach_alternative(html_message, "text/html")
        email.send()

        return Response({"message": "Password reset link has been sent!"}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    API endpoint to confirm password reset using a token.
    """
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Token is valid."}, status=status.HTTP_200_OK)

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

        form = SetPasswordForm(user, data=request.data)
        if form.is_valid():
            form.save()
            return Response({"detail": "Password successfully reset."}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
