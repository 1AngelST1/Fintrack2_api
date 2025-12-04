import os
import sys

# Construye rutas dentro del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- CARGA DE VARIABLES DE ENTORNO ---
try:
    from dotenv import load_dotenv
    # Busca el archivo .env explícitamente en la raíz del proyecto
    env_path = os.path.join(BASE_DIR, '.env')
    load_dotenv(env_path)
except ImportError:
    pass # Si no tienes python-dotenv instalado, esto se ignora silenciosamente

# SEGURIDAD
SECRET_KEY = os.getenv('SECRET_KEY', 'clave-segura-por-defecto-dev')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# HOSTS PERMITIDOS
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "AngelST.pythonanywhere.com"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Terceros
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'rest_auth',      # <--- CORREGIDO (Antes era django_rest_auth)
    'Fintrack2_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

# --- BASE DE DATOS BLINDADA ---
# El segundo valor en getenv es el valor por defecto para evitar el error 'NoneType'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', ''),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''), # Si esto falla, devuelve cadena vacía, no None
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

AUTH_USER_MODEL = 'Fintrack2_api.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRYPTO_PASSWORD = "clave-secreta-para-encriptacion-fintrack-cambiar-en-prod"
APPEND_SLASH = True