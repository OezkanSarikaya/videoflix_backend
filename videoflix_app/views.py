# from django.shortcuts import render

# Create your views here.
# videoflix_app/views.py
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Video, Genre, VideoProgress
from .serializers import VideoSerializer, GenreWithVideosSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
# from .permissions import IsAdminOrReadOnly
from rest_framework import permissions


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


# class VideoDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id, format=None):
#         try:
#             video = Video.objects.get(id=id)  # Hole Video anhand der ID
#             # Hier die Daten aus dem Video-Objekt formatieren
#             data = {
#                 "id": video.id,
#                 "title": video.title,
#                 "description": video.description,
#                 "video_file": video.video_file.url,
#                 "thumbnail": video.thumbnail.url,
#                 "created_at": video.created_at,
#             }
#             return Response(data)
#         except Video.DoesNotExist:
#             return Response(
#                 {"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND
#             )

class VideoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        video = get_object_or_404(Video, id=id)  # Holt das Video oder gibt automatisch 404 zurück

        data = {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "video_file": video.video_file.url if video.video_file else None,
            "thumbnail": video.thumbnail.url if video.thumbnail else None,
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
        video = get_object_or_404(Video, id=video_id)  # Holt das Video oder gibt 404 zurück
        progress = VideoProgress.objects.filter(user=request.user, video=video).first()

        return Response({"progress": progress.progress if progress else 0}, status=status.HTTP_200_OK)


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
                "video_file": request.build_absolute_uri(progress.video.video_file.url),
                "thumbnail": request.build_absolute_uri(progress.video.thumbnail.url),
                "progress": progress.progress,
            }
            for progress in user_progress
        ]

        return Response(video_data, status=status.HTTP_200_OK)
