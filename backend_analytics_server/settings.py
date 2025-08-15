"""
Django settings for backend_analytics_server project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- CONFIGURACIÓN DE SEGURIDAD PARA PRODUCCIÓN ---

# 1. Carga la SECRET_KEY desde las variables de entorno.
#    Es crucial para la seguridad en producción.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-_ff2#2pi^f7c^o9n$z($t4-b8^1l_n=&tf26g-r6v%7_ov@ft(' # Clave por defecto solo para desarrollo local
)

# 2. DEBUG se establece en False automáticamente en producción.
#    En Railway, la variable DEBUG no estará configurada como 'True', por lo que será False.
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# 3. Lógica robusta para ALLOWED_HOSTS y CSRF_TRUSTED_ORIGINS.
#    Esto soluciona cualquier 'IndexError' o problema de health check.
ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []

# Railway proporciona el dominio público en esta variable.
RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN')

# SOLO añadimos los hosts si estamos en un entorno de despliegue (es decir, la variable existe)
if RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.append(f".{RAILWAY_PUBLIC_DOMAIN}")
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_PUBLIC_DOMAIN}")
else:
    # Si no, asumimos que estamos en desarrollo local
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Para que WhiteNoise funcione en desarrollo con DEBUG=False
    'django.contrib.staticfiles',
    'dashboard',
    'security',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # WhiteNoise para servir estáticos
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


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [...]


# Internationalization
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
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