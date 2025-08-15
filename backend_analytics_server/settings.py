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
#    Esto soluciona el error 'IndexError'.
ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []

RAILWAY_STATIC_URL = os.environ.get('RAILWAY_STATIC_URL')
if RAILWAY_STATIC_URL:
    # Obtiene el hostname sin 'https://' para añadirlo a las listas
    hostname = RAILWAY_STATIC_URL.replace('https://', '').split(':')[0]
    ALLOWED_HOSTS.append(hostname)
    CSRF_TRUSTED_ORIGINS.append(f"https://{hostname}")

# Permite las pruebas locales si no estamos en Railway
if not RAILWAY_STATIC_URL:
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])
    CSRF_TRUSTED_ORIGINS.extend(['http://127.0.0.1:8000', 'http://localhost:8000'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'security', # <-- Asegúrate de que tu app 'security' esté registrada
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- WhiteNoise para servir estáticos
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
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-ec' # <-- Cambiado a español de Ecuador como ejemplo
TIME_ZONE = 'America/Guayaquil' # <-- Cambiado a zona horaria de Guayaquil
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración adicional para WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL de la API para obtener datos externos
LANDING_API_URL = 'http://cmaciasm.pythonanywhere.com/'

# --- CONFIGURACIÓN DE AUTENTICACIÓN ---
# Redirección si un usuario no autenticado intenta acceder a una vista protegida
LOGIN_URL = '/accounts/login/' # <-- Ruta estándar de Django

# Redirección después de un inicio de sesión exitoso
LOGIN_REDIRECT_URL = '/'

# Redirección después de un cierre de sesión exitoso
LOGOUT_REDIRECT_URL = '/accounts/login/'