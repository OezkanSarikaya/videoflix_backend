from rest_framework import serializers
from .models import Video, Genre, VideoProgress


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["id", "title", "description", "video_file", "thumbnail", "created_at"]


class GenreWithVideosSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True)

    class Meta:
        model = Genre
        fields = ["title", "videos"]


class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = ["user", "video", "progress", "updated_at"]
