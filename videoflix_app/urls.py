# videoflix_app/urls.py
from django.urls import path
from .views import VideoListView, GenreVideoListView, VideoDetailView

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video_list'),  # Liste der Videos
    path('videos/<int:id>/', VideoDetailView.as_view(), name='video_detail'),
    path('genres/videos/', GenreVideoListView.as_view(), name='genre_video_list'),
]
