"""
Django settings for videoflix_project project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Lade Umgebungsvariablen aus der .env-Datei
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'videoflix_app.apps.VideoflixAppConfig',
    'debug_toolbar',
    'django_rq',
    'import_export',
    'users',
]

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        # 'USERNAME': 'some-user',
        # 'PASSWORD': 'foobared',
        'DEFAULT_TIMEOUT': 360,
        # 'REDIS_CLIENT_KWARGS': {    # Eventual additional Redis connection arguments
        #     'ssl_cert_reqs': None,
        # },
    },
    # 'with-sentinel': {
    #     'SENTINELS': [('localhost', 26736), ('localhost', 26737)],
    #     'MASTER_NAME': 'redismaster',
    #     'DB': 0,
    #     # Redis username/password
    #     'USERNAME': 'redis-user',
    #     'PASSWORD': 'secret',
    #     'SOCKET_TIMEOUT': 0.3,
    #     'CONNECTION_KWARGS': {  # Eventual additional Redis connection arguments
    #         'ssl': True
    #     },
    #     'SENTINEL_KWARGS': {    # Eventual Sentinel connection arguments
    #         # If Sentinel also has auth, username/password can be passed here
    #         'username': 'sentinel-user',
    #         'password': 'secret',
    #     },
    # },
    # 'high': {
    #     'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'), # If you're on Heroku
    #     'DEFAULT_TIMEOUT': 500,
    # },
    # 'low': {
    #     'HOST': 'localhost',
    #     'PORT': 6379,
    #     'DB': 0,
    # }
}

# RQ_EXCEPTION_HANDLERS = ['path.to.my.handler'] # If you need custom exception handlers

INTERNAL_IPS = [
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
  'http://127.0.0.1:5500',
  'http://localhost:5500',
]

CORS_ALLOWED_ORIGINS = [
  'http://127.0.0.1:5500',
  'http://localhost:5500',
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "PASSWORD": "foobared",
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "videoflix"
    }
}

ROOT_URLCONF = 'videoflix_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'videoflix_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

IMPORT_EXPORT_USE_TRANSACTIONS = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
