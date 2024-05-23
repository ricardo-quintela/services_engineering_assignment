from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-k*_)&cl25a#cq=k6wi+-igqe(fi&f+4lzh8=(e7_x#9cfh0t46"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# elasticbeanstalk
EBS_HOST = os.environ.get(
    "EBS_HOST", "localhost"
)  # "django-env.eba-p3m7aa6p.us-east-1.elasticbeanstalk.com"
STEP_FUNCTION = os.environ.get("STEP_FUNCTION", "172.31.43.159")

# S3 buckets
S3_BUCKET_URL = os.environ.get("S3_BUCKET_URL", None)
S3_FRONTEND_BUCKET_NAME = os.environ.get("S3_FRONTEND_BUCKET_NAME", "frontend.clinic")
S3_IMAGE_BUCKET_NAME = os.environ.get("S3_IMAGE_BUCKET_NAME", "image.clinic")

# static applications
S3_STATIC_SITE_URL = os.environ.get("S3_STATIC_SITE_URL", "http://localhost:3000")
CLINIC_MONITOR_STATIC_SITE = os.environ.get(
    "CLINIC_MONITOR_STATIC_SITE", "http://localhost:3000"
)

# Rekognition
REKOGNITION_COLLECTION_ID = os.environ.get("REKOGNITION_COLLECTION_ID", "clinic.faces")

# State machine - Workflow
STATE_MACHINE_ARN = os.environ.get(
    "STATE_MACHINE_ARN",
    "arn:aws:states:us-east-1:123456789012:stateMachine:clinicStateMachine",
)

# RDS
RDS_NAME = os.environ.get("RDS_NAME", "rds.clinic")
RDS_HOST = os.environ.get("RDS_HOST", "localhost")
RDS_PORT = os.environ.get("RDS_PORT", "5432")
RDS_USER = os.environ.get("RDS_USER", "postgres")
RDS_PASSWORD = os.environ.get("RDS_PASSWORD", "postgres")


ALLOWED_HOSTS = [
    EBS_HOST,
    STEP_FUNCTION,
    CLINIC_MONITOR_STATIC_SITE,
    "18.208.0.153",
    "127.0.0.1",
    "172.31.4.96",
    "172.31.14.198",
]

CORS_ALLOWED_ORIGINS = [S3_STATIC_SITE_URL, CLINIC_MONITOR_STATIC_SITE]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["jwt", "content-type"]
CORS_EXPOSE_HEADERS = ["jwt"]


# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "authentication",
    "clinic",
    "appointments",
    "payment",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "clinic.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "clinic.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "USER": RDS_USER,
        "NAME": RDS_NAME,
        "PASSWORD": RDS_PASSWORD,
        "HOST": RDS_HOST,
        "PORT": RDS_PORT,
    },
    "testing": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


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

LANGUAGE_CODE = "pt"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# JWT Auth
JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXPIRY = 60 * 5

# Files
MAX_FILE_SIZE = 25 * 1024
