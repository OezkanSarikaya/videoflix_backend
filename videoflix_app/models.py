"""
Database models for the videoflix_app.
"""

from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from datetime import date
from django.conf import settings


class Genre(models.Model):
    """
    Represents a genre category for videos.
    """
    title = models.CharField(max_length=80, unique=True)

    class Meta:
        constraints = [
            UniqueConstraint(Lower("title"), name="unique_title_ci_genre")
        ]

    def __str__(self):
        return self.title


class Video(models.Model):
    """
    Represents a video with metadata, a file, and related genres.
    """
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to="videos", blank=True, null=True)
    thumbnail = models.FileField(upload_to="thumbnails", blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="videos")

    class Meta:
        constraints = [
            UniqueConstraint(Lower("title"), name="unique_title_ci_video")
        ]

    def __str__(self):
        return self.title


class VideoProgress(models.Model):
    """
    Tracks the user's progress for a specific video.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)  # Stores the position in seconds
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "video")

    def __str__(self):
        return f"Progress of {self.user} for video {self.video}"
