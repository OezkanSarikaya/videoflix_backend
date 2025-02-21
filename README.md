# Videoflix Backend

**[English Version](#english-version) | [Deutsche Version](#deutsche-version)**

---

## English Version

Videoflix is a video streaming platform inspired by Netflix.
This is a demo project as part of a training program.
The corresponding frontend can be found at [Videoflix Frontend](https://github.com/OezkanSarikaya/videoflix_frontend).

### Features
- Registration and login
- Password reset function
- Overview of all videos by genre
- Video streaming
- Manual resolution selection
- Automatic resolution adjustment based on screen width and loading time
- Save video progress to resume at the same position
- Watchlist: Overview of all videos with saved progress

### Requirements
- Python 3.10.12
- Django 5.1.4

### Installation on Linux System

#### 1. Clone the project
```bash
cd into_project_directory
git clone git@github.com:OezkanSarikaya/videoflix_backend.git
cd videoflix_backend
```

#### 2. Create a Virtual Environment
Create and activate a virtual Python environment:
```bash
python -m venv env
source env/bin/activate # Linux/Mac
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Create `.env` file
Create a `.env` file in the root directory following the `.env.template` template.

#### 5. Migrate the database
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Start the development server and create a superuser
```bash
python manage.py runserver
python manage.py createsuperuser
```

#### 7. Start Django worker
(Runs video conversions in the background. Requires Redis)
```bash
python manage.py rqworker
```

### 8. Import Videos

#### Import provided demo videos
1. Configure `.env` as per `.env.template`
2. Set `IMPORT_VIDEO_SOURCE=https://videoflix-backend.oezkan-sarikaya.de/demo_media/`
3. Run the import command:
   ```bash
   python import_videos.py --delete --source external
   ```

#### Import your own videos (local)
1. Create a folder under `demo_media` named `videos`
2. Place your video files there
3. Store your thumbnails in the `thumbnails` folder
4. Update `demo_media/demo.json` with your filenames
5. Run the import command:
   ```bash
   python import_videos.py --delete --source local
   ```

#### Import your own videos from an external URL
1. Configure `.env` with `IMPORT_VIDEO_SOURCE=your_url`
2. The folder structure under `demo_media` must include:
   - `thumbnails` (thumbnails)
   - `videos`
3. Place your files there
4. Update `demo_media/demo.json` with your filenames and entries
5. Run the import command:
   ```bash
   python import_videos.py --delete --source external
   ```

### 9. Add individual videos
1. Go to the administration area (Superuser required)
2. Navigate to `Videos` and click `Add`
3. Fill in the title and description
4. Select a thumbnail and a video file from the local directory
5. Choose one or more genres or create a new one
6. Click `Save`
7. The data will be added, and Django workers will convert the videos into four different resolutions
8. This process may take some time
9. Progress can be monitored at `/django-rq/`

[Go to German Version](#deutsche-version)

---

## Deutsche Version

Videoflix ist eine Video-Streaming-Plattform nach dem Vorbild von Netflix.
Es handelt sich um ein Demo-Projekt im Rahmen einer Weiterbildung.
Das dazugehörige Frontend ist unter [Videoflix Frontend](https://github.com/OezkanSarikaya/videoflix_frontend) zu finden.

### Funktionen
- Registrierung und Login
- Passwort-vergessen-Funktion
- Übersicht aller Videos nach Genre
- Streaming der Videos
- Manuelle Auswahl der Auflösung
- Automatische Einstellung der Auflösung auf Basis der Bildschirmbreite und Ladezeit
- Speicherung des Videofortschritts, um an der gleichen Stelle fortzusetzen
- Watchlist: Übersicht aller Videos mit gespeichertem Fortschritt

### Voraussetzungen
- Python 3.10.12
- Django 5.1.4

### Installation auf Linux-System

#### 1. Projekt klonen
```bash
cd in_den_Projektordner
git clone git@github.com:OezkanSarikaya/videoflix_backend.git
cd videoflix_backend
```

#### 2. Virtual Environment erstellen
Virtuelles Python-Umfeld erstellen und aktivieren:
```bash
python -m venv env
source env/bin/activate # Linux/Mac
```

#### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

#### 4. `.env` Datei anlegen
Nach Vorlage der `.env.template` eine `.env` Datei im Hauptverzeichnis erstellen.

#### 5. Datenbank migrieren
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Entwicklungsserver starten und Superuser erstellen
```bash
python manage.py runserver
python manage.py createsuperuser
```

#### 7. Django Worker starten
(Führt Video-Konvertierungen im Hintergrund aus. Erfordert Redis)
```bash
python manage.py rqworker
```

### 8. Videos importieren

#### So importieren Sie Demo-Videos
1. `.env` wie die Vorlage `.env.template` einrichten
2. Setzen Sie `IMPORT_VIDEO_SOURCE=https://videoflix-backend.oezkan-sarikaya.de/demo_media/`
3. Führen Sie den Import-Befehl aus:
   ```bash
   python import_videos.py --delete --source external
   ```

#### So importieren Sie eigene Videos (lokal)
1. Erstellen Sie einen Ordner unterhalb von `demo_media` mit dem Namen `videos`
2. Legen Sie Ihre Videodateien dort ab
3. Legen Sie Ihre Vorschaubilder im Ordner `thumbnails` ab
4. Aktualisieren Sie `demo_media/demo.json` mit Ihren Dateinamen
5. Führen Sie den Import-Befehl aus:
   ```bash
   python import_videos.py --delete --source local
   ```

[Zur englischen Version](#english-version)
