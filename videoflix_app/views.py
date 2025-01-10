# from django.shortcuts import render

# Create your views here.
# videoflix_app/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Video, Genre
from .serializers import VideoSerializer, GenreWithVideosSerializer

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]  # Nur authentifizierte Benutzer dürfen zugreifen

class GenreVideoListView(APIView):
    def get(self, request):
        genres = Genre.objects.prefetch_related('videos').all()
        serializer = GenreWithVideosSerializer(genres, many=True)
        return Response(serializer.data)

