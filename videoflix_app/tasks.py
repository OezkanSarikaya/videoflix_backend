import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)
ffmpeg_path = os.getenv("FFMPEG_PATH")

# Definiere die gewünschten Auflösungen
RESOLUTIONS = {
    "120p": "160x120",
    "360p": "640x360",
    "720p": "1280x720",
    "1080p": "1920x1080",
}

# Universelle Konvertierungsfunktion
def convert_video(source, resolution):
    source_path = Path(source)  # Betriebssystemunabhängig
    output_file = source_path.with_name(f"{source_path.stem}_{resolution}{source_path.suffix}")
    scale = RESOLUTIONS[resolution]

    # ffmpeg-Befehl
    cmd = [
        ffmpeg_path,
        "-i",
        str(source_path),
        "-vf",
        f"scale={scale}:force_original_aspect_ratio=decrease",
        "-c:v",
        "libx264",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-strict",
        "-2",
        str(output_file),
    ]

    # Führe ffmpeg aus und protokolliere die Ausgabe
    log_file = source_path.with_name(f"ffmpeg_{resolution}.log")
    with open(log_file, "w") as log:
        process = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)

    # Fehlerprüfung
    if process.returncode != 0:
        print(f"Conversion to {resolution} failed. Check {log_file} for details.")
    else:
        print(f"Conversion to {resolution} completed successfully.")

# Beispielaufrufe
def convert120p(source):
    convert_video(source, "120p")

def convert360p(source):
    convert_video(source, "360p")

def convert720p(source):
    convert_video(source, "720p")

def convert1080p(source):
    convert_video(source, "1080p")
