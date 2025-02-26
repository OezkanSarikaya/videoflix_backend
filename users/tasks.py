"""
Tasks for sending emails related to user authentication.
"""

from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
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
    html_message = render_to_string(
            "activate_account_email.html", {"user": user, "activation_link": activation_link}
        )
    
    plain_message = strip_tags(html_message)  # Entfernt HTML-Tags für die Plaintext-Version
    subject = "Activate your account"
    email = EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.attach_alternative(html_message, "text/html")  # HTML-Version anhängen

    # Senden der E-Mail
    email.send()   
