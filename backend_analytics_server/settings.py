# backend_analytics_server/settings.py

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

## --- CONFIGURACIÓN DE SEGURIDAD FINAL ---
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-_ff2#2pi^f7c^o9n$z($t4-b8^1l_n=&tf26g-r6v%7_ov@ft('
)

# DEBUG es False si la variable de entorno IS_PRODUCTION es 'True'
IS_PRODUCTION = os.environ.get('IS_PRODUCTION', 'False').lower() == 'true'
DEBUG = not IS_PRODUCTION

# Lista de hosts permitidos
ALLOWED_HOSTS = []

RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if IS_PRODUCTION and RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.append(f".{RAILWAY_PUBLIC_DOMAIN}")
else:
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])


# --- CSRF ---
CSRF_TRUSTED_ORIGINS = []
if IS_PRODUCTION and RAILWAY_PUBLIC_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https{RAILWAY_PUBLIC_DOMAIN}")


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_analytics_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend_analytics_server.wsgi.application'


# --- CONFIGURACIÓN DE BASE DE DATOS ---
# Usa la base de datos de Railway si está disponible, si no, usa SQLite local.
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=False)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
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
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True


# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL de la API para obtener datos externos
LANDING_API_URL = 'http://cmaciasm.pythonanywhere.com/'

# --- CONFIGURACIÓN DE AUTENTICACIÓN ---
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'