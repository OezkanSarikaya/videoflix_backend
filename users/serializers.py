"""
Serializers for user authentication and registration.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from .tasks import send_activation_email

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles user creation and sends an activation email.
    """
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        """
        Creates a new user with an inactive status and sends an activation email.
        """
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(str(user.pk).encode())
        token = default_token_generator.make_token(user)
        send_activation_email(user, uid, token)

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to add additional claims to JWT tokens.
    """

    @classmethod
    def get_token(cls, user):
        """
        Generates a JWT token with additional claims.
        """
        token = super().get_token(user)
        token["email"] = user.email  # Adds email to the token payload
        return token


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT tokens.
    """
    refresh = serializers.CharField()
    access = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.
    """
    email = serializers.EmailField()
