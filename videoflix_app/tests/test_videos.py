from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from ..models import Video
from django.urls import reverse


class VideoTests(APITestCase):
    def setUp(self):
        # Erstelle einen Admin-Benutzer
        self.admin_user = CustomUser.objects.create_user(
            email="admin@example.com",
            password="adminpassword",
            is_staff=True,
            is_active=True,
        )

        # Erstelle einen normalen Benutzer
        self.regular_user = CustomUser.objects.create_user(
            email="user@example.com", password="userpassword", is_active=True
        )

        # Erstelle ein Video (zum Testen)
        self.video_data = {
            "title": "Test Video",
            "description": "Test description",
            "video_file": None,  # Optional, je nach deinem Modell
            "thumbnail": None,  # Optional, je nach deinem Modell
        }

        self.video = Video.objects.create(
            title="Test Video",
            description="Ein Testvideo",
            video_file="test.mp4",
            thumbnail="test.jpg",
        )

        self.url = "/api/videos/"

    def test_list_videos_regular_user(self):
        """GET /videos mit Authentifizierung → 200"""
        # self.client.force_authenticate(user=self.user)
        self.client.login(email="user@example.com", password="userpassword")
        url = reverse("video_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_videos_unauthenticated(self):
        """GET /videos ohne Authentifizierung → 401"""
        url = reverse("video_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_video_detail_regular_user(self):
        """GET /videos/<id>/ mit Authentifizierung → 200"""
        self.client.login(email="user@example.com", password="userpassword")
        url = reverse("video_detail", kwargs={"id": self.video.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_video_detail_unauthenticated(self):
        """GET /videos/<id>/ ohne Authentifizierung → 401"""
        url = reverse("video_detail", kwargs={"id": self.video.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_video_authenticated(self):
        # Teste die Erstellung eines Videos als Admin
        self.client.login(email="admin@example.com", password="adminpassword")
        response = self.client.post(
            self.url + "create/", self.video_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_video_unauthenticated(self):
        # Teste die Erstellung eines Videos ohne Authentifizierung
        response = self.client.post(
            self.url + "create/", self.video_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_video_regular_user(self):
        # Teste die Erstellung eines Videos als normaler Benutzer
        self.client.login(email="user@example.com", password="userpassword")
        response = self.client.post(
            self.url + "create/", self.video_data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Nur Admins dürfen

    def test_update_video_authenticated(self):
        # Teste das Aktualisieren eines Videos als Admin
        video = Video.objects.create(**self.video_data)
        update_data = {"title": "Updated Test Video"}
        self.client.login(email="admin@example.com", password="adminpassword")
        response = self.client.put(
            f"{self.url}{video.id}/update/", update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_video_unauthenticated(self):
        # Teste das Aktualisieren eines Videos ohne Authentifizierung
        video = Video.objects.create(**self.video_data)
        update_data = {"title": "Updated Test Video"}
        response = self.client.put(
            f"{self.url}{video.id}/update/", update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_video_regular_user(self):
        # Teste das Aktualisieren eines Videos als normaler Benutzer
        video = Video.objects.create(**self.video_data)
        update_data = {"title": "Updated Test Video"}
        self.client.login(email="user@example.com", password="userpassword")
        response = self.client.put(
            f"{self.url}{video.id}/update/", update_data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Nur Admins dürfen

    def test_delete_video_authenticated(self):
        # Teste das Löschen eines Videos als Admin
        video = Video.objects.create(**self.video_data)
        self.client.login(email="admin@example.com", password="adminpassword")
        response = self.client.delete(f"{self.url}{video.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_video_unauthenticated(self):
        # Teste das Löschen eines Videos als Admin
        video = Video.objects.create(**self.video_data)
        response = self.client.delete(f"{self.url}{video.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_video_regular_user(self):
        # Teste das Löschen eines Videos als normaler Benutzer
        video = Video.objects.create(**self.video_data)
        self.client.login(email="user@example.com", password="userpassword")
        response = self.client.delete(f"{self.url}{video.id}/delete/")
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Nur Admins dürfen
