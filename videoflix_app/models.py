from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from datetime import date
from django.conf import settings

# Create your models here.


class Genre(models.Model):
    title = models.CharField(max_length=80)

    class Meta:
        constraints = [UniqueConstraint(Lower("title"), name="unique_title_ci_genre")]

    def __str__(self):
        return self.title 


class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to="videos", blank=True, null=True)
    thumbnail = models.FileField(upload_to="thumbnails", blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="videos")

    class Meta:
        constraints = [UniqueConstraint(Lower("title"), name="unique_title_ci_video")]

    def __str__(self):
        return self.title


class VideoProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey("Video", on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)  # Speichert die Position in Sekunden
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "video")

    def __str__(self):
        return f"Progress of {self.user} for video {self.video}"
