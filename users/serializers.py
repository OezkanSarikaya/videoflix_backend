from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
# Falls du eine separate Task verwendest, um die E-Mail zu senden.
from .tasks import send_activation_email

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        # Benutzer erstellen
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = False
        user.save()

        # Generiere den UID und Token
        uid = urlsafe_base64_encode(str(user.pk).encode())
        token = default_token_generator.make_token(user)

        # Sende die Aktivierungs-E-Mail
        send_activation_email(user, uid, token)

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token['email'] = user.email
        return token


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class JWTSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


# Passwort zurücksetzen
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
