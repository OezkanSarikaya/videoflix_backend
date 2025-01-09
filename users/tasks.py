from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_activation_email(user, uid, token):
    # activation_link = f"http://localhost:4200/activate/{uid}/{token}/"
    activation_link = f"http://localhost:4200/activate/?uid={uid}&token={token}"
    # activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"
    subject = "Activate your account"
    message = f"Hi {user.email},\n\nPlease click the link below to activate your account:\n{activation_link}"
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

# def send_password_reset_email(user, uid, token):
#     # activation_link = f"http://localhost:4200/activate/{uid}/{token}/"
#     activation_link = f"http://localhost:4200/activate/?uid={uid}&token={token}"
#     # activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"
#     subject = "Reset your passwort"
#     message = f"Hi {user.email},\n\nPlease click the link below to reset your password:\n{activation_link}"
    
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
