import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# FFMPEG path from environment variables
ffmpeg_path = os.getenv("FFMPEG_PATH")

# Define the resolutions and their corresponding scale values
RESOLUTIONS = {
    "120p": "160x120",     # Very low resolution
    "360p": "640x360",     # Low resolution
    "720p": "1280x720",    # HD resolution
    "1080p": "1920x1080",  # Full HD resolution
}

def convert_video(source, resolution):
    """
    Converts a video to a specific resolution using ffmpeg.
    
    :param source: The path to the source video file
    :param resolution: The desired target resolution (e.g., '720p')
    """
    source_path = Path(source)  # Ensure the path works across operating systems
    output_file = source_path.with_name(f"{source_path.stem}_{resolution}{source_path.suffix}")  # Generate new filename
    scale = RESOLUTIONS.get(resolution)  # Get the scale value from the dictionary

    if not scale:
        print(f"Error: Unknown resolution '{resolution}'")
        return

    # ffmpeg command to convert the video
    cmd = [
        ffmpeg_path,
        "-i", str(source_path),
        "-vf", f"scale={scale}:force_original_aspect_ratio=decrease",
        "-c:v", "libx264",
        "-crf", "23",  # Quality (lower value = better quality)
        "-c:a", "aac",
        "-strict", "-2",  # AAC audio codec
        str(output_file)
    ]

    # Run the ffmpeg command and save the output to a log file
    log_file = source_path.with_name(f"ffmpeg_{resolution}.log")
    with open(log_file, "w") as log:
        process = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)

    # Error handling based on the return code of ffmpeg
    if process.returncode != 0:
        print(f"Conversion to {resolution} failed. Check {log_file} for details.")
    else:
        print(f"Conversion to {resolution} completed successfully.")

# Individual functions for each resolution
def convert120p(source):
    """Convert video to 120p resolution."""
    convert_video(source, "120p")

def convert360p(source):
    """Convert video to 360p resolution."""
    convert_video(source, "360p")

def convert720p(source):
    """Convert video to 720p resolution."""
    convert_video(source, "720p")

def convert1080p(source):
    """Convert video to 1080p resolution."""
    convert_video(source, "1080p")
