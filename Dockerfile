# Verwenden von Python 3.12.0
FROM python:3.12.0-slim

# Installiere Systempakete, die für PostgreSQL und FFmpeg notwendig sind
RUN apt-get update && apt-get install -y \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis setzen
WORKDIR /usr/src/videoflix

# Kopiere den gesamten Projektordner in den Container
COPY . /usr/src/videoflix/

# Installiere Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Sammle statische Dateien
RUN python manage.py collectstatic --noinput

# Setze den Standardbefehl zum Starten der Django-Anwendung (beispielsweise Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "videoflix_project.wsgi:application"]

