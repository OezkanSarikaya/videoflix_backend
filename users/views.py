from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from .serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    JWTSerializer,
    PasswordResetSerializer,
)
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import JsonResponse
from dotenv import load_dotenv
from pathlib import Path
import os
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


FRONTEND_URL = os.getenv("FRONTEND_URL")

User = get_user_model()


def activate_account(request, uidb64, token):
    try:
        # Dekodiere die UID und den Token
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        token_generator = default_token_generator
        if token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return JsonResponse({"message": "Account erfolgreich aktiviert!"})
        else:
            return HttpResponse("Token ist ungültig", status=400)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        return HttpResponse("Ungültiger Link", status=400)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Versuche, den Benutzer zu erstellen
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Account erfolgreich erstellt."},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Fehler, wenn die E-Mail bereits registriert ist
        except IntegrityError:
            return Response(
                {"detail": "Email already registered."}, status=status.HTTP_409_CONFLICT
            )

        # Andere Fehler
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    """
    Benutzer können ihre E-Mail-Adresse eingeben und erhalten einen Reset-Link per E-Mail.
    """

    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Es gibt keinen Benutzer mit dieser E-Mail-Adresse."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generiere Token und uid
        uid = urlsafe_base64_encode(str(user.pk).encode())
        token = default_token_generator.make_token(user)
        reset_link = f"{FRONTEND_URL}reset-password/{uid}/{token}/" 

        subject = "Passwort zurücksetzen"
        
        html_message = render_to_string(
            "password_reset_email.html",
            {
                "user": user,
                "reset_link": reset_link,
            },
        )
        plain_message = strip_tags(html_message)  # Entfernt HTML-Tags für die Text-Version

        email = EmailMultiAlternatives(
            subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email]
        )
        email.attach_alternative(html_message, "text/html")  # HTML-Version hinzufügen
        email.send()

        return Response(
            {"message": "Passwort-Zurücksetzungslink wurde gesendet!"},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response(
                {"detail": "Ungültiger Token oder Benutzer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Token ist ungültig oder abgelaufen."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"detail": "Token ist gültig."}, status=status.HTTP_200_OK)

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response(
                {"detail": "Ungültiger Token oder Benutzer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Token ist ungültig oder abgelaufen."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Das neue Passwort wird vom Frontend übermittelt
        form = SetPasswordForm(user, data=request.data)
        if form.is_valid():
            form.save()
            return Response(
                {"detail": "Passwort erfolgreich zurückgesetzt."},
                status=status.HTTP_200_OK,
            )
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
