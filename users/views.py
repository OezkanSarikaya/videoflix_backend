from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from .serializers import UserRegistrationSerializer, LoginSerializer, JWTSerializer, PasswordResetSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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
            return HttpResponse('Account erfolgreich aktiviert!')
        else:
            return HttpResponse('Token ist ungültig', status=400)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        return HttpResponse('Ungültiger Link', status=400)

# User Registration View
class UserRegistrationView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account erstellt. Bitte überprüfe deine E-Mails, um deinen Account zu aktivieren."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View
class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                return Response({
                    'access': str(access_token),
                    'refresh': str(refresh),
                })
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Password Reset
class PasswordResetView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode()).decode()
                send_mail(
                    'Passwort zurücksetzen',
                    render_to_string('email/reset_password_email.html', {
                        'uid': uid,
                        'token': token,
                    }),
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email]
                )
                return Response({"message": "E-Mail für die Passwort-Wiederherstellung gesendet."}, status=status.HTTP_200_OK)
            return Response({"error": "Benutzer nicht gefunden"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Password Reset Confirm
class PasswordResetConfirmView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid')
        token = request.data.get('token')
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(request.data['password'])
                user.save()
                return Response({"message": "Passwort erfolgreich zurückgesetzt."}, status=status.HTTP_200_OK)
            return Response({"error": "Token ungültig oder abgelaufen."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

