from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )  # Optional für den User, wird aber durch E-Mail ersetzt
    # custom = models.CharField(max_length=500, default="")
    # address = models.CharField(max_length=150, default="")
    # phone = models.CharField(max_length=25, default="")
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # Verwende E-Mail als primären Login
    REQUIRED_FIELDS = [
        "password"
    ]  # Hier 'username' beibehalten, auch wenn er optional ist

    objects = CustomUserManager()  # Verknüpfe den CustomUserManager

    def __str__(self):
        return self.email
