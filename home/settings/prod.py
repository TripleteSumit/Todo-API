import os
from .base import *

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = []


STATIC_ROOT = os.path.join(BASE_DIR, "static")

CORS_ALLOWED_ORIGINS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("MYSQL_DATABASE"),
        "HOST": os.environ.get("MYSQL_DATABASE_HOST"),
        "USER": os.environ.get("MYSQL_DATABASE_USER_NAME"),
        "PASSWORD": os.environ.get("MYSQL_ROOT_PASSWORD"),  # "Sumit@Dey",
        "PORT": "3306",
    }
}
