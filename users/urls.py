from django.urls import path
from .views import UserRegistrationView, LoginView, PasswordResetView, PasswordResetConfirmView, activate_account

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='user_signup'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('activate/<uidb64>/<token>/', activate_account, name='account-activate'),
]
