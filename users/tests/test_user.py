from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse("user_signup")
        self.login_url = reverse("token_obtain_pair")
        self.token_refresh_url = reverse("token_refresh")
        self.password_reset_url = reverse("password_reset")
        
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
        
    # Weitere Tests für Passwort-Reset-Bestätigung & Kontoaktivierung können hier ergänzt werden.
