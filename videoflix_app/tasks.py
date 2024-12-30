import subprocess
import os
from pathlib import Path

def convert720p(source):

    # ffmpeg_path = "C:/usr/ffmpeg/bin/ffmpeg.exe"  # Auf Linux wird 'ffmpeg' direkt im PATH erwartet
    ffmpeg_path = os.getenv('ffmpeg_path')
    source_path = Path(source)  # Betriebssystemunabhängig
    new_file_name = source_path.with_name(f"{source_path.stem}_720p{source_path.suffix}")    
 
    cmd = f'"{ffmpeg_path}" -i "{source_path}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'

    run = subprocess.run(cmd, capture_output=True)
 
