"""
Serializers for the videoflix_app models.
"""

from rest_framework import serializers
from .models import Video, Genre
from django.conf import settings


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model, including formatted thumbnail and video file URLs.
    """
    thumbnail = serializers.SerializerMethodField()
    video_file = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        """
        Returns the full URL for the video thumbnail.
        """
        return f"{settings.PROTECTED_MEDIA_URL}{obj.thumbnail.name}"

    def get_video_file(self, obj):
        """
        Returns the full URL for the video file.
        """
        return f"{settings.PROTECTED_MEDIA_URL}{obj.video_file.name}"

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "description",
            "video_file",
            "thumbnail",
            "created_at",
        ]


class GenreWithVideosSerializer(serializers.ModelSerializer):
    """
    Serializer for the Genre model with a list of associated videos.
    """
    videos = VideoSerializer(many=True)

    class Meta:
        model = Genre
        fields = ["title", "videos"]
