from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Nutzt eine In-Memory-Datenbank für schnellere Tests
    }
}
