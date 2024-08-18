from .base import *

DEBUG = True

SECRET_KEY = "django-insecure-%=o2zubygpr!%br0z8=a#+m=#sxec241#=7%r=gm^fqu2ue@y="

ALLOWED_HOSTS = []


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]

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
