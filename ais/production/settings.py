"""
This is the settings file to be used in a production environment. It's
more secure, more robust and more performant than the development setup
and also configures AIS to talk to external services.
"""

import os
from ais.common.settings import *

SECRET_KEY = os.environ.get("SECRET_KEY")
# This is important so other people can't set their own domains
# to point to AIS (which would be a security concern).
ALLOWED_HOSTS = [".armada.nu", "localhost", "armada.nu"]

DEBUG = False

# The URL scheme is slightly different in a production environment
# since we need to accomodate the KTH OpenID Connect integration.
ROOT_URLCONF = "ais.production.urls"

# Use a full-fledged database instead of SQLite.
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("DB_NAME", "ais_dev"),
        "USER": os.environ.get("DB_USERNAME", "ais_dev"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "ais_dev"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# SENTRY
RAVEN_CONFIG = {
    "dsn": "https://%s:%s@sentry.io/%s"
    % (
        os.environ.get("SENTRY_USERNAME"),
        os.environ.get("SENTRY_PASSWORD"),
        os.environ.get("SENTRY_APPID"),
    ),
    "processors": ("raven.processors.Processor",),
}

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "sentry": {
            "level": "ERROR",  # To capture more than ERROR, change to WARNING, INFO, etc.
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
            "tags": {"custom-tag": "x"},
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "root": {
            "level": "WARNING",
            "handlers": ["sentry"],
        },
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "raven": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# The system sends out system-related emails to these addresses.
ADMINS = MANAGERS = (("System", "system@armada.nu"),)
