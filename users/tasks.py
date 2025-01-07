from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_activation_email(user, uid, token):
    activation_link = f"http://127.0.0.1:8000/api/users/activate/{uid}/{token}/"
    # activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"
    subject = "Activate your account"
    message = f"Hi {user.email},\n\nPlease click the link below to activate your account:\n{activation_link}"
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
