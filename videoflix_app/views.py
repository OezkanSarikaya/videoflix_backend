from rest_framework import generics
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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def serve_protected_media(request: Request, path):
    """Serve media files only to authenticated users with JWT."""

    # Authenticate the user
    auth = JWTAuthentication()
    user, _ = auth.authenticate(request)
    if not user:
        raise Http404("Unauthorized")

    # Check file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(file_path):
        raise Http404("File not found.")

    return FileResponse(open(file_path, "rb"))


class VideoCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only admins can create videos

    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Create video
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only admins can update videos

    def put(self, request, id, *args, **kwargs):
        video = get_object_or_404(Video, id=id)
        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Update video
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only admins can delete videos

    def delete(self, request, id, *args, **kwargs):
        video = get_object_or_404(Video, id=id)
        video.delete()  # Delete video
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access


class VideoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        video = get_object_or_404(Video, id=id)  # Retrieve video or return 404

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
        # Get the video ID and the user from the request
        video_id = request.data.get("video")
        user = request.user

        # Fetch the video object or return 404 if not found
        video = get_object_or_404(Video, id=video_id)

        # Get or create VideoProgress object
        progress, created = VideoProgress.objects.get_or_create(user=user, video=video)

        # Get the progress value from the request data
        progress_value = request.data.get("progress", 0)

        try:
            # Attempt to convert progress_value to an integer
            progress_value = int(progress_value)
        except ValueError:
            return Response(
                {"error": "Progress must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate that the progress value is between 0 and 100
        if not (0 <= progress_value <= 100):
            return Response(
                {"error": "Progress must be between 0 and 100."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save the progress
        progress.progress = progress_value
        progress.save()

        return Response(
            {"status": "success", "progress": progress.progress},
            status=status.HTTP_201_CREATED,
        )


class VideoProgressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id, *args, **kwargs):
        video = get_object_or_404(Video, id=video_id)  # Retrieve video or return 404
        progress = VideoProgress.objects.filter(user=request.user, video=video).first()

        return Response(
            {"progress": progress.progress if progress else 0},
            status=status.HTTP_200_OK,
        )


class VideoProgressListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve all progress for the current user
        user_progress = VideoProgress.objects.filter(user=request.user).select_related(
            "video"
        )

        # Create a list with video data
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
