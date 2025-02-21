from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    """
    Custom user model that uses email as the unique identifier for authentication
    instead of a username.
    """
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )  # Optional field, replaced by email
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # Use email as the primary login field
    REQUIRED_FIELDS = []  # No additional required fields

    objects = CustomUserManager()  # Link to the custom user manager

    def __str__(self):
        """
        Return the string representation of the user (email).
        """
        return self.email
