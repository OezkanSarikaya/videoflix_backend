from django.urls import path
from .views import (
    VideoListView,                # View for listing all videos
    GenreVideoListView,           # View for listing videos by genre
    VideoDetailView,              # View for displaying video details
    VideoProgressView,            # View for saving video progress
    VideoProgressDetailView,      # View for retrieving progress of a specific video
    VideoProgressListView,        # View for listing all video progress
    VideoCreateView,              # View for creating a new video
    VideoUpdateView,              # View for updating a video
    VideoDeleteView,              # View for deleting a video
)

urlpatterns = [
    path("videos/", VideoListView.as_view(), name="video_list"),  # List all videos
    path("videos/<int:id>/", VideoDetailView.as_view(), name="video_detail"),  # View details of a specific video
    path("videos/create/", VideoCreateView.as_view(), name="video_create"),  # Create a new video
    path("videos/<int:id>/update/", VideoUpdateView.as_view(), name="video_update"),  # Update a specific video
    path("videos/<int:id>/delete/", VideoDeleteView.as_view(), name="video_delete"),  # Delete a specific video
    path("genres/videos/", GenreVideoListView.as_view(), name="genre_video_list"),  # List videos filtered by genre
    # Endpoint to save video progress (POST request)
    path("video-progress/", VideoProgressView.as_view(), name="video-progress"),
    # Endpoint to retrieve the progress of a specific video (GET request)
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
