import os
import shutil
import django
import argparse
from dotenv import load_dotenv
import urllib.request

# Django-Projekt initialisieren
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix_project.settings')
django.setup()

from videoflix_app.models import Video, Genre, VideoProgress
from import_export.formats.base_formats import JSON

# .env-Datei laden
load_dotenv()

# CLI-Argumente definieren
parser = argparse.ArgumentParser(description="Importiert Videos in die Datenbank.")
parser.add_argument("--delete", action="store_true", help="Bestehende Videos vor dem Import löschen.")
parser.add_argument("--source", choices=["local", "external"], default="local", help="Legt fest, ob Videos aus einer lokalen Quelle oder einer externen URL geladen werden.")
args = parser.parse_args()

# Medienpfade definieren
DEMO_MEDIA_PATH = os.path.join(os.getcwd(), "demo_media")
MEDIA_PATH = os.path.join(os.getcwd(), "media")

# URL der externen Quelle aus der .env-Datei laden
EXTERNAL_SOURCE_URL = os.getenv("IMPORT_VIDEO_SOURCE", "")

# Pfad zur Demo-JSON-Datei
demo_file = os.path.join(DEMO_MEDIA_PATH, "demo.json")

def download_file(url, destination):
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"✅ Erfolgreich heruntergeladen: {destination}")
    except Exception as e:
        print(f"⚠️ Fehler beim Herunterladen {url}: {e}")

# Falls --delete gesetzt ist, alle bestehenden Daten löschen
if args.delete:
    print("🔴 Lösche bestehende Videos, Genres und Fortschritte...")
    Video.objects.all().delete()
    Genre.objects.all().delete()
    VideoProgress.objects.all().delete()

# Importiere die Demo-Daten
with open(demo_file, "r") as f:
    dataset = JSON().create_dataset(f.read())

for row in dataset.dict:
    # Erstelle oder hole das Video-Objekt
    video, created = Video.objects.get_or_create(
        title=row["title"],
        description=row["description"],
        # created_at=row["created_at"],
    )

    # Verknüpfe Genres mit dem Video
    for genre_title in row["genres"]:
        genre, _ = Genre.objects.get_or_create(title=genre_title)
        video.genres.add(genre)

    # Dateipfade aus der JSON übernehmen
    video_file = row["video_file"]
    thumbnail = row["thumbnail"]

    if args.source == "external":
        video_url = os.path.join(EXTERNAL_SOURCE_URL, video_file)
        thumbnail_url = os.path.join(EXTERNAL_SOURCE_URL, thumbnail)

        video_file_dest = os.path.join(MEDIA_PATH, video_file)
        thumbnail_dest = os.path.join(MEDIA_PATH, thumbnail)

        download_file(video_url, video_file_dest)
        download_file(thumbnail_url, thumbnail_dest)

        video.video_file.name = video_file  # Relativen Pfad speichern
        video.thumbnail.name = thumbnail      

    else:
        # Lokale Dateien kopieren
        video_file_src = os.path.join(DEMO_MEDIA_PATH, video_file)
        video_file_dest = os.path.join(MEDIA_PATH, video_file)

        thumbnail_src = os.path.join(DEMO_MEDIA_PATH, thumbnail)
        thumbnail_dest = os.path.join(MEDIA_PATH, thumbnail)        

        if os.path.exists(video_file_src):
            os.makedirs(os.path.dirname(video_file_dest), exist_ok=True)
            shutil.copy(video_file_src, video_file_dest)

            print(f"Kopiere -> {video_file_dest}")  # Debug-Print
            video.video_file.name = video_file  # ← Hier nur den relativen Pfad speichern
        else:
            print(f"⚠️ Video-Datei nicht gefunden: {video_file_src}")

        if os.path.exists(thumbnail_src):
            os.makedirs(os.path.dirname(thumbnail_dest), exist_ok=True)
            shutil.copy(thumbnail_src, thumbnail_dest)

            print(f"Kopiere -> {thumbnail_dest}")  # Debug-Print
            video.thumbnail.name = thumbnail  # ← Hier auch nur den relativen Pfad speichern
        else:
            print(f"⚠️ Thumbnail-Datei nicht gefunden: {thumbnail_src}")

    # Speichere das Video
    video.save()

print("✅ Import abgeschlossen!")
