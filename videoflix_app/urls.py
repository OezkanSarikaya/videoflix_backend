from django.urls import path
from .views import (
    VideoListView,
    GenreVideoListView,
    VideoDetailView,
    VideoProgressView,
    VideoProgressDetailView,
    VideoProgressListView,
    VideoCreateView,
    VideoUpdateView,
    VideoDeleteView,
)


urlpatterns = [
    path("videos/", VideoListView.as_view(), name="video_list"),
    path("videos/<int:id>/", VideoDetailView.as_view(), name="video_detail"),
    path("videos/create/", VideoCreateView.as_view(), name="video_create"),
    path("videos/<int:id>/update/", VideoUpdateView.as_view(), name="video_update"),
    path("videos/<int:id>/delete/", VideoDeleteView.as_view(), name="video_delete"),
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
