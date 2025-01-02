from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from datetime import date
# from .models import Genre

# Create your models here.

class Genre(models.Model):    
    title = models.CharField(max_length=80)   

    class Meta:
        constraints = [
          UniqueConstraint(
                Lower('title'),
                name='unique_title_ci'
            )
        ]     

    def __str__(self):
        return self.title

class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)  
    thumbnail = models.FileField(upload_to='thumbnails', blank=True, null=True) 
    genres = models.ManyToManyField(Genre, related_name="videos")      

    def __str__(self):
        return self.title
    

