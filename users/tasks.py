from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv
from pathlib import Path
import os

# env_path = Path(__file__).resolve().parent.parent / ".env"
# load_dotenv(env_path)

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")
print(f"Frontend URL: {FRONTEND_URL}")


def send_activation_email(user, uid, token):
    activation_link = f"{FRONTEND_URL}activate/?uid={uid}&token={token}"
    # activation_link = f"{FRONTEND_URL}reset-password/{uid}/{token}/"
    # activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"
    subject = "Activate your account"
    message = f"Hi {user.email},\n\nPlease click the link below to activate your account:\n{activation_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
