import os
import django
import json

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix_project.settings')
django.setup()

# Import models
from videoflix_app.models import Video, Genre

# Define export data list
data = []

# Loop through all videos and gather necessary data
for video in Video.objects.prefetch_related('genres'):
    genres = [genre.title for genre in video.genres.all()]  # Collect genres for each video
    video_data = {
        "title": video.title,
        "description": video.description,
        "video_file": video.video_file.name if video.video_file else None,
        "thumbnail": video.thumbnail.name if video.thumbnail else None,
        "genres": genres,
    }
    data.append(video_data)

# Export the data to a JSON file
EXPORT_FILE_PATH = "export.json"  # Define the export file path
try:
    with open(EXPORT_FILE_PATH, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"✅ Videos successfully exported to {EXPORT_FILE_PATH}!")
except Exception as e:
    print(f"⚠️ Error during export: {e}")
