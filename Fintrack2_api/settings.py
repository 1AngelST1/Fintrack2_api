import os
from pathlib import Path
import sys

# Construye rutas dentro del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- INTENTAR CARGAR VARIABLES DE ENTORNO ---
# Esto ayuda a que lea el archivo .env tanto en local como en producción si usas python-dotenv
try:
    from dotenv import load_dotenv
    env_path = os.path.join(BASE_DIR, '.env')
    load_dotenv(env_path)
except ImportError:
    pass

# ADVERTENCIA DE SEGURIDAD: usa variables de entorno
# Si no encuentra la variable, usa una clave insegura por defecto (solo para dev)
SECRET_KEY = os.getenv('SECRET_KEY', '-_&+lsebec(whhw!%n@ww&1j=4-^j_if9x8$q778+99oz&!ms2')

# DEBUG: Lee del .env. Si dice "True" es verdadero, si no, falso.
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS: Importante agregar tu dominio de PythonAnywhere
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "AngelST.pythonanywhere.com"]

# Definición de aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Librerías de terceros
    'django_filters',                 # Necesarios para los filtros de DRF
    'rest_framework',                 # API Rest
    'rest_framework.authtoken',       # Soporte de tokens
    'corsheaders',                    # Manejo de CORS
    'django_rest_auth',               # (Parece que lo tenías en requirements.txt)
    # Tu aplicación principal
    'Fintrack2_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',     # IMPORTANTE: CORS antes de Common
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de CORS
# Lee la variable del .env y la convierte en lista
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:4200').split(',')
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'Fintrack2_api.urls'

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

WSGI_APPLICATION = 'Fintrack2_api.wsgi.application'

# --- BASE DE DATOS CORREGIDA ---
# Ahora usa las variables que definiste en tu .env en PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

# CONFIGURACIÓN DE USUARIO PERSONALIZADO
AUTH_USER_MODEL = 'Fintrack2_api.CustomUser'

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --- ARCHIVOS ESTÁTICOS (CORREGIDO) ---
STATIC_URL = '/static/'
# Esta línea faltaba y causaba el error de ImproperlyConfigured
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Archivos Media
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Configuración de Django Rest Framework
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Clave requerida por tu archivo cypher_utils.py
CRYPTO_PASSWORD = "clave-secreta-para-encriptacion-fintrack-cambiar-en-prod"

# Manejo de 'Trailing Slash'
APPEND_SLASH = True