import os

# Construye rutas dentro del proyecto así: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ADVERTENCIA DE SEGURIDAD: mantén la clave secreta usada en producción en secreto
SECRET_KEY = '-_&+lsebec(whhw!%n@ww&1j=4-^j_if9x8$q778+99oz&!ms2'

# ADVERTENCIA DE SEGURIDAD: no ejecutes con debug activado en producción
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

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
    'corsheaders',                    # Manejo de CORS (conexión con Angular)
    # Tu aplicación principal (donde están tus models.py, views, etc.)
    'Fintrack2_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',     # IMPORTANTE: CORS debe ir antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de CORS: permite que Angular (puerto 4200) haga peticiones
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
]
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'Fintrack2_api.urls'

# Configuración de Plantillas (Templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # Puedes agregar os.path.join(BASE_DIR, 'templates') si usas HTML
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

# Base de Datos
# Asegúrate de que el archivo my.cnf existe en la raíz y tiene tus credenciales
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, "my.cnf"),
            'charset': 'utf8mb4',
        }
    }
}

# [cite_start]CONFIGURACIÓN DE USUARIO PERSONALIZADO [cite: 53]
# Esto le dice a Django que use tu modelo CustomUser en lugar del default
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

# Archivos Estáticos
STATIC_URL = '/static/'

# Archivos Media
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Configuración de Django Rest Framework
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

# --- CORRECCIÓN AQUÍ ---
# Esta línea va AFUERA del diccionario, al final del archivo
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'