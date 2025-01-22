import os
import shutil
import django

# Django-Projekt initialisieren
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix_project.settings')
django.setup()

from videoflix_app.models import Video, Genre, VideoProgress
from import_export.formats.base_formats import JSON

# Pfade definieren
DEMO_MEDIA_PATH = os.path.join(os.getcwd(), 'demo_media')
MEDIA_PATH = os.path.join(os.getcwd(), 'media')

# Pfad zur Demo-JSON-Datei
demo_file = os.path.join(DEMO_MEDIA_PATH, 'demo.json')

# Lösche alle bestehenden Videos und Genres
Video.objects.all().delete()
Genre.objects.all().delete()
VideoProgress.objects.all().delete()

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

    # Dateipfade aus der JSON übernehmen
    video_file = row['video_file']
    thumbnail = row['thumbnail']

    # Erstelle den vollständigen Quell- und Zielpfad
    video_file_src = os.path.join(DEMO_MEDIA_PATH, video_file)
    video_file_dest = os.path.join(MEDIA_PATH, video_file)

    thumbnail_src = os.path.join(DEMO_MEDIA_PATH, thumbnail)
    thumbnail_dest = os.path.join(MEDIA_PATH, thumbnail)

    # Kopiere die Dateien
    if os.path.exists(video_file_src):
        os.makedirs(os.path.dirname(video_file_dest), exist_ok=True)
        shutil.copy(video_file_src, video_file_dest)
        video.video_file.name = video_file
    else:
        print(f"Video-Datei nicht gefunden: {video_file_src}")

    if os.path.exists(thumbnail_src):
        os.makedirs(os.path.dirname(thumbnail_dest), exist_ok=True)
        shutil.copy(thumbnail_src, thumbnail_dest)
        video.thumbnail.name = thumbnail
    else:
        print(f"Thumbnail-Datei nicht gefunden: {thumbnail_src}")

    # Speichere das Video
    video.save()

print("Import abgeschlossen!")
