"""
Django settings for devserver project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "%e75-a0m25%0oze*rub(o-7j8wou7z!6$9m7xz#do3e1cgve%g"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["dev.vryhof.net", "dev.vryhof.local"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.amazon",
    "allauth.socialaccount.providers.bitbucket",
    "allauth.socialaccount.providers.digitalocean",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.nextcloud",
    "django_extensions",
    "rest_framework",
    "bootstrap4",
    "music.apps.DevConfig",
    "frontend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
SOCIALACCOUNT_PROVIDERS = {
    "amazon": {
    },
    "bitbucket": {
    },
    "digitalocean": {
    },
    "github": {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    },
    'nextcloud': {
        'SERVER': 'https://nextcloud.vryhof.net',
    }
}

ROOT_URLCONF = "devserver.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"), os.path.join(BASE_DIR, "frontend", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "devserver.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "dev",
        "USER": "dev",
        "PASSWORD": "dev",
        "HOST": "dev",
        "PORT": 5432,
        "CONN_MAX_AGE": 600,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
SONG_CACHE_PATH = os.path.join(MEDIA_ROOT, "song_cache")

ERROR_LOG = os.path.join(os.path.dirname(BASE_DIR), "logs", "error.log")

try:
    LOGGER_LEVEL = os.environ["LOGGER_LEVEL"]
except KeyError:
    LOGGER_LEVEL = "ERROR"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s %(levelname)s [%(name)s: %(pathname)s %(funcName)s line:%(lineno)s] -- %(message)s",
            "datefmt": "%m-%d-%Y %H:%M:%S",
        },
        "verbose": {"format": "%(asctime)s %(levelname)s %(name)s -- %(message)s", "datefmt": "%m-%d-%Y %H:%M:%S"},
        "simple": {"format": "%(asctime)s %(levelname)s %(message)s"},
    },
    "handlers": {
        "weather": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(os.path.dirname(BASE_DIR), "logs", "weather.log"),
            "maxBytes": 1024 * 1024 * 100,  # 100 mb
            "backupCount": 3,
        },
        "file": {"level": LOGGER_LEVEL, "class": "logging.FileHandler", "filename": ERROR_LOG},
    },
    "loggers": {
        "": {"level": "INFO", "handlers": ["weather"], "propagate": True},
        "django": {"handlers": ["file"], "level": LOGGER_LEVEL, "propagate": True},
    },
}

# MUSIC_FOLDER = os.path.join("/", "mnt", "net", "nas2", "Music")
MUSIC_FOLDER = os.path.join("/", "home", "avryhof", "Music")