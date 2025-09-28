# backend_condominio/settings.py
from pathlib import Path
from datetime import timedelta
import environ
from corsheaders.defaults import default_headers  # ← para añadir Authorization

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

# --- Seguridad / entorno ---
SECRET_KEY = env("SECRET_KEY", default="dev-key")
DEBUG = env.bool("DEBUG", default=False)  # ← producción: False por defecto

# Solo tu host de backend (Render)
ALLOWED_HOSTS = ["smart-condominio-backend.onrender.com"]

# --- Apps ---
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",

    # Tus apps
    "administradores",
    "copropietarios",
    "visitantes",
    "guardias",
    "casas",
    "vehiculos",
    "mascotas",
]

AUTH_USER_MODEL = "administradores.Administrador"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # protegido por defecto
    ],
}
# Nota: tus vistas públicas (p.ej. /auth/login/) deben declarar AllowAny.

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

COPROPIETARIO_JWT_SECRET = SECRET_KEY
COPROPIETARIO_ACCESS_LIFETIME = timedelta(days=7)

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",           # ← CORS antes de Common/WhiteNoise
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- CORS / CSRF ---
# Origen del FRONTEND (Netlify)
CORS_ALLOWED_ORIGINS = [
    "https://smart-condominio.netlify.app",
]

# Si usarás cookies/sesión cross-site:
# CORS_ALLOW_CREDENTIALS = True

# Permite Authorization para JWT
CORS_ALLOW_HEADERS = list(default_headers) + [
    "Authorization",
    "Content-Type",
    "X-CSRFToken",
]

# Sitios confiables para CSRF (si haces POST desde el FE)
CSRF_TRUSTED_ORIGINS = [
    "https://smart-condominio.netlify.app",
    # (opcional) tu propio backend también es seguro
    "https://smart-condominio-backend.onrender.com",
]

ROOT_URLCONF = "backend_condominio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend_condominio.wsgi.application"

# --- Base de datos (Neon/Postgres) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT", default="5432"),
        "OPTIONS": {"sslmode": "require"},
    }
}

# --- Passwords ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- i18n ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static ---
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
