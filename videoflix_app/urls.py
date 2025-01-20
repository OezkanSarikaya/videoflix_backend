# videoflix_app/urls.py
from django.urls import path
from .views import (
    VideoListView,
    GenreVideoListView,
    VideoDetailView,
    VideoProgressView,
    VideoProgressDetailView,
    VideoProgressListView,
)

urlpatterns = [
    path("videos/", VideoListView.as_view(), name="video_list"),  # Liste der Videos
    path("videos/<int:id>/", VideoDetailView.as_view(), name="video_detail"),
    path("genres/videos/", GenreVideoListView.as_view(), name="genre_video_list"),
    # Endpunkt zum Speichern des Fortschritts (POST-Anfrage)
    path("video-progress/", VideoProgressView.as_view(), name="video-progress"),
    # Endpunkt zum Abrufen des Fortschritts eines bestimmten Videos (GET-Anfrage)
    path(
        "video-progress/<int:video_id>/",
        VideoProgressDetailView.as_view(),
        name="video-progress-detail",
    ),
    path(
        "video-progress-list/",
        VideoProgressListView.as_view(),
        name="video-progress-list",
    ),
]
