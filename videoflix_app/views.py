# from django.shortcuts import render

# Create your views here.
# videoflix_app/views.py
from rest_framework import generics

# from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Video, Genre, VideoProgress
from .serializers import VideoSerializer, GenreWithVideosSerializer
from rest_framework import status
from django.http import FileResponse, Http404
import os
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.conf import settings

# from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

# from rest_framework import serializers


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def serve_protected_media(request: Request, path):
    """Serviert Medien-Dateien nur für authentifizierte Nutzer mit JWT."""

    # Ist der User authentifiziert?
    auth = JWTAuthentication()
    user, _ = auth.authenticate(request)
    if not user:
        raise Http404("Nicht autorisiert")

    # Datei-Pfad prüfen
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(file_path):
        raise Http404("Datei nicht gefunden.")

    return FileResponse(open(file_path, "rb"))


class VideoCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Nur Admins dürfen Videos erstellen

    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Video erstellen
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Nur Admins dürfen Videos updaten

    def put(self, request, id, *args, **kwargs):
        video = get_object_or_404(Video, id=id)
        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Video aktualisieren
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Nur Admins dürfen Videos löschen

    def delete(self, request, id, *args, **kwargs):
        video = get_object_or_404(Video, id=id)
        video.delete()  # Video löschen
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Nur authentifizierte Benutzer dürfen zugreifen


class VideoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        video = get_object_or_404(
            Video, id=id
        )  # Holt das Video oder gibt automatisch 404 zurück

        data = {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "video_file": f"{settings.PROTECTED_MEDIA_URL}{video.video_file}",
            "thumbnail": f"{settings.PROTECTED_MEDIA_URL}{video.thumbnail.name}",
            "created_at": video.created_at,
        }
        return Response(data)


class GenreVideoListView(APIView):
    def get(self, request):
        genres = Genre.objects.prefetch_related("videos").all()
        serializer = GenreWithVideosSerializer(genres, many=True)
        return Response(serializer.data)


class VideoProgressView(APIView):
    def post(self, request, *args, **kwargs):
        # Überprüfen, ob der Fortschritt bereits existiert
        video_id = request.data.get("video")
        user = request.user

        video = get_object_or_404(Video, id=video_id)
        progress, created = VideoProgress.objects.get_or_create(user=user, video=video)

        # Speichern des Fortschritts
        progress.progress = request.data.get("progress", 0)
        progress.save()

        return Response(
            {"status": "success", "progress": progress.progress},
            status=status.HTTP_201_CREATED,
        )


class VideoProgressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id, *args, **kwargs):
        video = get_object_or_404(
            Video, id=video_id
        )  # Holt das Video oder gibt 404 zurück
        progress = VideoProgress.objects.filter(user=request.user, video=video).first()

        return Response(
            {"progress": progress.progress if progress else 0},
            status=status.HTTP_200_OK,
        )


class VideoProgressListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Hole alle Fortschritte des aktuellen Benutzers
        user_progress = VideoProgress.objects.filter(user=request.user).select_related(
            "video"
        )

        # Erstelle eine Liste mit den Video-Daten
        video_data = [
            {
                "id": progress.video.id,
                "title": progress.video.title,
                "description": progress.video.description,
                "video_file": f"{settings.PROTECTED_MEDIA_URL}{progress.video.video_file.url}",
                "thumbnail": f"{settings.PROTECTED_MEDIA_URL}{progress.video.thumbnail.name}",
                "progress": progress.progress,
            }
            for progress in user_progress
        ]

        return Response(video_data, status=status.HTTP_200_OK)
