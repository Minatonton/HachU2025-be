import os

from .base import *  # noqa: F403
from .utils import strtobool

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-b9ar4o1oz2ez^o@d*vw2-9+te*8cgvejc5ae1j_s4i@x(+-0jc",
)

DEBUG = strtobool(os.getenv("DEBUG", "y"))

CORS_ALLOW_ALL_ORIGINS = DEBUG

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        # "app_name": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        # }
    },
}

if strtobool(os.getenv("DEBUG_SQL", "n")):
    LOGGING["loggers"]["django.db.backends"] = {
        "handlers": ["console"],
        "level": "DEBUG",
    }

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += [  # noqa: F405
    "rest_framework.authentication.SessionAuthentication",
]
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += [  # noqa: F405
    "rest_framework.renderers.BrowsableAPIRenderer",
]
