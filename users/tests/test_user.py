from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()

# def decode_jwt(jwt_token):
#     # JWT besteht aus drei Teilen, getrennt durch '.'
#     try:
#         # Token in drei Teile aufsplitten (Header, Payload, Signature)
#         parts = jwt_token.split('.')
        
#         # Der Payload ist der zweite Teil (Index 1) und muss Base64-dekodiert werden
#         payload = base64.urlsafe_b64decode(parts[1] + '==')  # Füge '==' hinzu, um Base64 korrekt zu dekodieren
        
#         # Payload in ein JSON-Objekt umwandeln
#         return json.loads(payload)
#     except Exception as e:
#         return str(e)

class UserTests(APITestCase):


    def setUp(self):
        self.signup_url = reverse("user_signup")
        self.login_url = reverse("token_obtain_pair")
        self.token_refresh_url = reverse("token_refresh")
        self.password_reset_url = reverse("password_reset")
        self.password_reset_confirm_url = "password_reset_confirm"         
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="TestPass123",
            is_active=True
        )
    
    def test_signup(self):
        data = {
            "email": "newuser@example.com",
            "password": "NewPass123",
            "username": "newuser"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data = {"email": "testuser@example.com", "password": "TestPass123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        login_response = self.client.post(self.login_url, {"email": "testuser@example.com", "password": "TestPass123"})
        refresh_token = login_response.data["refresh"]
        response = self.client.post(self.token_refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_password_reset_request(self):
        data = {"email": "testuser@example.com"}
        response = self.client.post(self.password_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        # Test für ungültige Login-Daten
        data = {"email": "testuser@example.com", "password": "WrongPassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def test_account_activation(self):
        uid = urlsafe_base64_encode(str(self.user.pk).encode())
        token = default_token_generator.make_token(self.user)
        activation_url = reverse("account_activate", kwargs={"uidb64": uid, "token": token})

        response = self.client.get(activation_url)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.is_active)

    def test_invalid_account_activation(self):
        uid = urlsafe_base64_encode(str(9999).encode())  # ungültige User-ID
        token = "invalidtoken"
        activation_url = reverse("account_activate", kwargs={"uidb64": uid, "token": token})

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_confirm_valid_token(self):
        uid = urlsafe_base64_encode(str(self.user.pk).encode())
        token = default_token_generator.make_token(self.user)
        password_reset_confirm_url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})

        new_password_data = {"new_password1": "NewTestPass123", "new_password2": "NewTestPass123"}
        response = self.client.post(password_reset_confirm_url, new_password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewTestPass123"))

    def test_password_reset_confirm_invalid_token(self):
        uid = urlsafe_base64_encode(str(self.user.pk).encode())
        token = "invalidtoken"
        password_reset_confirm_url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})

        new_password_data = {"new_password1": "NewTestPass123", "new_password2": "NewTestPass123"}
        response = self.client.post(password_reset_confirm_url, new_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    # def test_custom_token_contains_email_claim(self):
    #     # Teste, ob der benutzerdefinierte Claim 'email' im access-Token enthalten ist
    #     data = {"email": "testuser@example.com", "password": "TestPass123"}
    #     response = self.client.post(self.login_url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    #     # Extrahiere und dekodiere den access-Token
    #     access_token = response.data["access"]
    #     decoded_payload = decode_jwt(access_token)
        
    #     # Überprüfe, ob der 'email' Claim im Payload enthalten ist
    #     self.assertIn("email", decoded_payload)
    #     self.assertEqual(decoded_payload["email"], "testuser@example.com")

    
        
    # Weitere Tests für Passwort-Reset-Bestätigung & Kontoaktivierung können hier ergänzt werden.
