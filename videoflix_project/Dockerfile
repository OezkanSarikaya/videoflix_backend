# Basis-Image
FROM python:3.10-slim

# Arbeitsverzeichnis in Container setzen
WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    ffmpeg \
    supervisor && \
    rm -rf /var/lib/apt/lists/*

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Dateien kopieren
COPY . .

# Statische Dateien sammeln
RUN python manage.py collectstatic --noinput

# Gunicorn als Standardbefehl
CMD ["gunicorn", "videoflix_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "5"]
