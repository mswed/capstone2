from .settings import *  # We import our existing settings
from decouple import config

# Override the database entry
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "name": "grumpytracker_test_db",
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
        "CONN_MAX_AGE": 0,  # We close the connection after each request
        "TEST": {"NAME": "test_grumpytracker_test_db"},
    }
}

# Override the media root
MEDIA_ROOT = BASE_DIR / "test_media"
MEDIA_URL = "/test_media"

DEBUG = True
TESTING = True
