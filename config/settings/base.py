from pathlib import Path
from dotenv import load_dotenv
from os import path, getenv
from loguru import logger
from datetime import timedelta, date
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APP_DIR = BASE_DIR / "core_apps"

local_env_file = path.join(BASE_DIR, ".envs", ".local.env")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites", # Allows to have multiple sites
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_countries",
    "phonenumber_field",
    "drf_spectacular",
    "django_filters",
    "djoser",
    "cloudinary",
    "djcelery_email",
    "django_celery_beat",
]

LOCAL_APPS = [
    "core_apps.user_auth",
    "core_apps.common",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core_apps.user_auth.middleware.CustomHeaderMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APP_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DB"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": getenv("POSTGRES_HOST"),
        "PORT": getenv("POSTGRES_PORT"),
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "user_auth.CustomUser"
# Defaults for the profiles
DEFAULT_BIRTH_DATE = date(2000, 1, 1)
DEFAULT_DATE_JOINED = date(2021, 1, 1)
DEFAULT_EXPIRY_DATE = date(2024, 1, 1)
DEFAULT_COUNTRY = "US"
DEFAULT_PHONE_NUMBER = "+593 994233890"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Django Banking API",
    "DESCRIPTION": "Django Banking API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "LICENSE": {
        "name": "MIT License",
        "url": "https://opensource.org/license/mit",
    }
}

if USE_TZ:
    # Ensures scheduled tasks run accordingly to our tz
    CELERY_TIMEZONE = TIME_ZONE

# Broker: where celery gets the tasks
CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
# Where celery stores results of the tasks
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")

# Serialization settings
# Which format the worker accepts
CELERY_ACCEPT_CONTENT = ["application/json"]
# How tasks are serialized
CELERY_TASK_SERIALIZER = "json"
# How results are serialized
CELERY_RESULT_SERIALIZER = "json"

# Result Backend Retry & Extensions
# If the backend temporarily fails, Celery retries up to 10 times to fetch/store results.
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# When True, result objects include more metadata (like task start time, runtime, etc.).
CELERY_RESULT_EXTENDED = True
# Always retry connecting to the backend if there’s an error.
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True

# Task Time Limits
# If the task still hasn’t stopped, Celery force kills it.
CELERY_TASK_TIME_LIMIT = 5 * 60
# After 5 minutes, the task gets a SoftTimeLimitExceeded exception
CELERY_TASK_SOFT_TIME_LIMIT = 5 * 60

# Tells Celery Beat to use the database to store periodic task schedules instead of a local file.
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Workers will send task events (e.g., started, succeeded, failed) 
# so monitoring tools (like flower) can track them in real time.
CELERY_WORKER_SEND_TASK_EVENTS = True

CLOUDINARY_CLOUD_NAME = getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

LOGGING_CONFIG = None # Avoid conflicts with loguru

LOGURU_LOGGING ={
    "handlers": [
        {
            "sink": BASE_DIR / "logs/debug.log", # Debug logs file
            "level": "DEBUG", # Anything above DEBUG lvl will be sent to the file
            "filter": lambda record: record["level"].no <= logger.level("WARNING").no,
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - "
            "{message}",
            "rotation": "10 MB",
            "retention": "30 days",
            "compression": "zip",
        },
        {
            "sink": BASE_DIR / "logs/error.log", # Debug logs file
            "level": "ERROR", # Anything above DEBUG lv will be sent to the file
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - "
            "{message}",
            "rotation": "10 MB",
            "retention": "30 days",
            "compression": "zip",
            "backtrace": True,
            "diagnose": True,
        },
    ],
}

logger.configure(**LOGURU_LOGGING)

LOGGING = {
    "version":1,
    "disable_existing_loggers": False,
    "handlers": {"loguru":{"class": "interceptor.InterceptHandler"}},
    "root": {"handlers": ["loguru"], "level": "DEBUG"},
}

