import os
import django

# Django-Projekt initialisieren
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix_project.settings')
django.setup()

from videoflix_app.models import Video, Genre
from import_export.formats.base_formats import JSON

# Pfad zur Demo-JSON-Datei
demo_file = os.path.join('demo_media', 'demo.json')

# Lösche alle bestehenden Videos und zugehörigen Genres
Video.objects.all().delete()
Genre.objects.all().delete()

# Importiere die Demo-Daten
with open(demo_file, 'r') as f:
    dataset = JSON().create_dataset(f.read())

for row in dataset.dict:
    # Erstelle oder hole das Video-Objekt
    video, created = Video.objects.get_or_create(
        title=row['title'],
        description=row['description'],
        created_at=row['created_at']
    )

    # Verknüpfe Genres mit dem Video
    for genre_title in row['genres']:
        genre, _ = Genre.objects.get_or_create(title=genre_title)
        video.genres.add(genre)

    # Setze die Pfade zu den Mediendateien
    video.video_file.name = f"demo_media/videos/{row['video_file']}"
    video.thumbnail.name = f"demo_media/thumbnails/{row['thumbnail']}"
    video.save()

print("Import abgeschlossen!")
