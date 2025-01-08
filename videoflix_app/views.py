# from django.shortcuts import render

# Create your views here.
# videoflix_app/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Video
from .serializers import VideoSerializer

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]  # Nur authentifizierte Benutzer dürfen zugreifen

