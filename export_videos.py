import os
import django
import json

# Django-Umgebung konfigurieren
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix_project.settings')
django.setup()

# Modelle importieren
from videoflix_app.models import Video, Genre

# Videos exportieren
data = []
for video in Video.objects.prefetch_related('genres'):
    genres = [genre.title for genre in video.genres.all()]
    video_data = {
        "title": video.title,
        "description": video.description,
        "video_file": video.video_file.name if video.video_file else None,
        "thumbnail": video.thumbnail.name if video.thumbnail else None,
        "created_at": str(video.created_at),
        "genres": genres,
    }
    data.append(video_data)

# Export in eine JSON-Datei
with open("export.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Videos erfolgreich exportiert!")


