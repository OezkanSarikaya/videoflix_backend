"""
Tasks for sending emails related to user authentication.
"""

from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")


def send_activation_email(user, uid, token):
    """
    Sends an activation email to the user with a verification link.

    Args:
        user (CustomUser): The user object.
        uid (str): The user's encoded ID.
        token (str): The generated activation token.
    """
    if not FRONTEND_URL:
        raise ValueError("FRONTEND_URL is not set in the environment variables.")

    activation_link = f"{FRONTEND_URL}activate/?uid={uid}&token={token}"
    subject = "Activate your account"
    message = f"Hi {user.email},\n\nPlease click the link below to activate your account:\n{activation_link}"

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
