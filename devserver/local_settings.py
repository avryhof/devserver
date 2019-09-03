from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "dev",
        "USER": "dev",
        "PASSWORD": "dev",
        "HOST": "192.168.1.133",
        "PORT": 5432,
        "CONN_MAX_AGE": 600,
    }
}

MUSIC_FOLDER = os.path.join("Z:", "Music")