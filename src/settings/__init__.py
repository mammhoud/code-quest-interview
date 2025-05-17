# flake8: noqa
# isort: skip_file

from pathlib import Path

from src.env import CURRENT_ENV, Environment

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


if CURRENT_ENV == Environment.DEVELOPMENT:
    DEBUG = True
else:
    DEBUG = False
DEBUG = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/


ROOT_URLCONF = "core.urls"

WSGI_APPLICATION = "src.wsgi.application"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1

from .security import *
from .apps import *
from .i18n import *
from .database import *
from .auth import *
from .middleware import *
from .templates import *
from .rest import *
from .migrations import *
from .logger import *

from .debug_toolbar import *
