import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

def convert720p(source):   
    ffmpeg_path  = os.getenv('FFMPEG_PATH')       
    source_path = Path(source)  # Betriebssystemunabhängig
    new_file_name = source_path.with_name(f"{source_path.stem}_720p{source_path.suffix}")    
 
    cmd = f'"{ffmpeg_path }" -i "{source_path}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'

    run = subprocess.run(cmd, capture_output=True)
 
