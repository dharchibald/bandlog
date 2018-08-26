from settings import BASE_DIR, PROJECT_ROOT
import os

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "test",
        "USER": "user",
        "PASSWORD": "anoynmous",
        "HOST": "localhost",
        "PORT": "",
    }
}
