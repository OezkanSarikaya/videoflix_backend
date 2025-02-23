import os
import shutil
import django
import argparse
from dotenv import load_dotenv
import urllib.request
from import_export.formats.base_formats import JSON
from videoflix_app.models import Video, Genre, VideoProgress

# Initialize Django project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix_project.settings')
django.setup()

# Load environment variables from the .env file
load_dotenv()

# Define CLI arguments for video import
parser = argparse.ArgumentParser(description="Import videos into the database.")
parser.add_argument("--delete", action="store_true", help="Delete existing videos before import.")
parser.add_argument("--source", choices=["local", "external"], default="local", help="Specify if videos are loaded from a local source or external URL.")
args = parser.parse_args()

# Define media paths
DEMO_MEDIA_PATH = os.path.join(os.getcwd(), "demo_media")
MEDIA_PATH = os.path.join(os.getcwd(), "media")

# Load external source URL from .env file
EXTERNAL_SOURCE_URL = os.getenv("IMPORT_VIDEO_SOURCE", "")

# Path to the demo JSON file
demo_file = os.path.join(DEMO_MEDIA_PATH, "demo.json")

def download_file(url, destination):
    """Download file from URL to the specified destination."""
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"✅ Successfully downloaded: {destination}")
    except Exception as e:
        print(f"⚠️ Error downloading {url}: {e}")

# Delete existing data if --delete flag is passed
if args.delete:
    print("🔴 Deleting existing videos, genres, and progress...")
    Video.objects.all().delete()
    Genre.objects.all().delete()
    VideoProgress.objects.all().delete()

# Import demo data from JSON file
with open(demo_file, "r") as f:
    dataset = JSON().create_dataset(f.read())

for row in dataset.dict:
    # Create or retrieve video object
    video, created = Video.objects.get_or_create(
        title=row["title"],
        description=row["description"],
    )

    # Link genres to video
    for genre_title in row["genres"]:
        genre, _ = Genre.objects.get_or_create(title=genre_title)
        video.genres.add(genre)

    # Get file paths from JSON data
    video_file = row["video_file"]
    thumbnail = row["thumbnail"]

    # Handle external source (e.g., download from URL)
    if args.source == "external":
        video_url = os.path.join(EXTERNAL_SOURCE_URL, video_file)
        thumbnail_url = os.path.join(EXTERNAL_SOURCE_URL, thumbnail)

        video_file_dest = os.path.join(MEDIA_PATH, video_file)
        thumbnail_dest = os.path.join(MEDIA_PATH, thumbnail)

        # Download video and thumbnail files
        download_file(video_url, video_file_dest)
        download_file(thumbnail_url, thumbnail_dest)

        # Save relative file paths to the video object
        video.video_file.name = video_file
        video.thumbnail.name = thumbnail

    else:
        # Handle local source (copy files locally)
        video_file_src = os.path.join(DEMO_MEDIA_PATH, video_file)
        video_file_dest = os.path.join(MEDIA_PATH, video_file)

        thumbnail_src = os.path.join(DEMO_MEDIA_PATH, thumbnail)
        thumbnail_dest = os.path.join(MEDIA_PATH, thumbnail)

        # Copy video file if it exists
        if os.path.exists(video_file_src):
            os.makedirs(os.path.dirname(video_file_dest), exist_ok=True)
            shutil.copy(video_file_src, video_file_dest)

            print(f"Copying -> {video_file_dest}")  # Debug print
            video.video_file.name = video_file
        else:
            print(f"⚠️ Video file not found: {video_file_src}")

        # Copy thumbnail file if it exists
        if os.path.exists(thumbnail_src):
            os.makedirs(os.path.dirname(thumbnail_dest), exist_ok=True)
            shutil.copy(thumbnail_src, thumbnail_dest)

            print(f"Copying -> {thumbnail_dest}")  # Debug print
            video.thumbnail.name = thumbnail
        else:
            print(f"⚠️ Thumbnail file not found: {thumbnail_src}")

    # Save the video object
    video.save()

print("✅ Import completed!")
