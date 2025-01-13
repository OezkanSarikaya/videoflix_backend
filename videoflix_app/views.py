# from django.shortcuts import render

# Create your views here.
# videoflix_app/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Video, Genre
from .serializers import VideoSerializer, GenreWithVideosSerializer
from rest_framework import status


class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Nur authentifizierte Benutzer dürfen zugreifen


class VideoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            video = Video.objects.get(id=id)  # Hole Video anhand der ID
            # Hier die Daten aus dem Video-Objekt formatieren
            data = {
                "id": video.id,
                "title": video.title,
                "description": video.description,
                "video_file": video.video_file.url,
                "thumbnail": video.thumbnail.url,
                "created_at": video.created_at,
            }
            return Response(data)
        except Video.DoesNotExist:
            return Response(
                {"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND
            )


class GenreVideoListView(APIView):
    def get(self, request):
        genres = Genre.objects.prefetch_related("videos").all()
        serializer = GenreWithVideosSerializer(genres, many=True)
        return Response(serializer.data)
