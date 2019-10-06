from .settings import *

SITE_ID = 1
ALLOWED_HOSTS = ["127.0.0.1"]

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

OLD_MUSIC_FOLDER = os.path.join("/", "mnt", "net", "nas2", "Music")
MUSIC_FOLDER = os.path.join("/", "home", "avryhof", "Music")
