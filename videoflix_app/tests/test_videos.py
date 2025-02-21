from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from ..models import Video, Genre, VideoProgress
from django.urls import reverse
from django.utils.crypto import get_random_string

def get_unique_title():
    return f"Test Video {get_random_string(8)}"


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

   
        # unique_title = get_unique_title()

        # Erstelle ein Video (zum Testen)
        self.video_data = {
            "title": get_unique_title(),
            "description": "Test description",
            "video_file": None,  # Optional, je nach deinem Modell
            "thumbnail": None,  # Optional, je nach deinem Modell
        }

        self.genre = Genre.objects.create(title="Action")

        self.video = Video.objects.create(
            title=get_unique_title(),
            description="Ein Testvideo",
            video_file="test.mp4",
            thumbnail="test.jpg",
        )

        self.invalid_video_data = {
            "description": "Ein tolles Video",
            "video_file": None,
            "thumbnail": None,
            "genres": [],  # Falls Genres erforderlich sind, könnte das auch ein Fehler auslösen
        }

        self.video.genres.set([self.genre])

        self.video_progress = VideoProgress.objects.create(
            user=self.regular_user, video=self.video, progress=50
        )

        self.url = "/api/videos/"
        self.genre_videos_url = "/api/genres/videos/"
        self.video_progress_url = "/api/video-progress/"
        self.video_progress_detail_url = f"/api/video-progress/{self.video.id}/"
        self.video_progress_list_url = "/api/video-progress-list/"

    def test_genre_videos_authenticated(self):
        """GET /genres/videos/ → Erfolgreich für authentifizierte Nutzer"""
        self.client.login(username="user@example.com", password="userpassword")
        response = self.client.get(self.genre_videos_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_videos_unauthenticated(self):
        """GET /genres/videos/ → Verweigert für nicht angemeldete Nutzer"""
        response = self.client.get(self.genre_videos_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_save_video_progress_authenticated(self):
        """POST /video-progress/ → Speichert Fortschritt für authentifizierte Nutzer"""
        self.client.login(username="user@example.com", password="userpassword")
        data = {"video": self.video.id, "progress": 80}
        response = self.client.post(self.video_progress_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_save_video_progress_unauthenticated(self):
        """POST /video-progress/ → Verweigert für nicht angemeldete Nutzer"""
        data = {"video": self.video.id, "progress": 80}
        response = self.client.post(self.video_progress_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_video_progress_authenticated(self):
        """GET /video-progress/<video_id>/ → Gibt Fortschritt für authentifizierte Nutzer zurück"""
        self.client.login(username="user@example.com", password="userpassword")
        response = self.client.get(self.video_progress_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["progress"], 50)  # Fortschritt sollte 50 sein

    def test_get_video_progress_unauthenticated(self):
        """GET /video-progress/<video_id>/ → Verweigert für nicht angemeldete Nutzer"""
        response = self.client.get(self.video_progress_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_video_progress_list_authenticated(self):
        """GET /video-progress-list/ → Gibt Liste zurück für authentifizierte Nutzer"""
        self.client.login(username="user@example.com", password="userpassword")
        response = self.client.get(self.video_progress_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_video_progress_list_unauthenticated(self):
        """GET /video-progress-list/ → Verweigert für nicht angemeldete Nutzer"""
        response = self.client.get(self.video_progress_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_videos_regular_user(self):
        """GET /videos mit Authentifizierung → 200"""
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

    def test_video_create_bad_request(self):
        # Teste die Erstellung eines Videos als Admin
        self.client.login(email="admin@example.com", password="adminpassword")
        response = self.client.post(
            self.url + "create/", self.invalid_video_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
        update_data = {"title": get_unique_title()}
        self.client.login(email="admin@example.com", password="adminpassword")
        response = self.client.put(
            f"{self.url}{video.id}/update/", update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_video_authenticated_bad_request(self):
        # Teste das Aktualisieren eines Videos als Admin
        video = Video.objects.create(**self.video_data)
        update_data = {"title": ""}
        self.client.login(email="admin@example.com", password="adminpassword")
        response = self.client.put(
            f"{self.url}{video.id}/update/", update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_video_unauthenticated(self):
        # Teste das Aktualisieren eines Videos ohne Authentifizierung
        video = Video.objects.create(**self.video_data)
        update_data = {"title": get_unique_title()}
        response = self.client.put(
            f"{self.url}{video.id}/update/", update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_video_regular_user(self):
        # Teste das Aktualisieren eines Videos als normaler Benutzer
        video = Video.objects.create(**self.video_data)
        update_data = {"title": get_unique_title()}
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

    def test_genre_str(self):
        """Testet die __str__ Methode für Genres mit einem Titel"""
        self.assertEqual(str(self.genre), "Action")

    def test_video_str(self):
        """Testet die __str__ Methode für Genres mit einem Titel"""
        video = Video.objects.create(title="Test Video")
        self.assertEqual(str(video), "Test Video")

    def test_video_progress_str_method(self):
        """Testet die __str__-Methode von VideoProgress"""
        expected_str = f"Progress of {self.regular_user} for video {self.video}"
        self.assertEqual(str(self.video_progress), expected_str)
