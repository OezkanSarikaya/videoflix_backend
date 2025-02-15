from rest_framework import serializers
from .models import Video, Genre
from django.conf import settings


class VideoSerializer(serializers.ModelSerializer):

    # Hier wird das Thumbnail richtig formatiert
    thumbnail = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        # Hier fügt man den korrekten URL-Pfad hinzu
        return f"{settings.PROTECTED_MEDIA_URL}{obj.thumbnail.name}"

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
    videos = VideoSerializer(many=True)

    class Meta:
        model = Genre
        fields = ["title", "videos"]
