"""
This is the settings file to be used in a production environment. It's
more secure, more robust and more performant than the development setup
and also configures AIS to talk to external services (e.g. CAS).
"""

import os
from os import environ as env
from ais.common.settings import *
from ais.secrets import *

# This is important so other people can't set their own domains
# to point to AIS (which would be a security concern).
ALLOWED_HOSTS = ['.armada.nu', 'localhost']

# The URL scheme is slightly different in a production environment
# since we need to accomodate the CAS integration.
ROOT_URLCONF = 'ais.production.urls'

# Use KTH CAS for authentication
INSTALLED_APPS += ('cas', 'raven.contrib.django.raven_compat',)
AUTHENTICATION_BACKENDS += ('cas.backends.CASBackend',)
CAS_SERVER_URL = 'https://login.kth.se/'
CAS_AUTO_CREATE_USER = False
CAS_RESPONSE_CALLBACKS = ('lib.CAS_callback.callback',)

# Use a full-fledged database instead of SQLite.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DB_NAME,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
    }
}

# SENTRY
RAVEN_CONFIG = {
    'dsn': 'https://%s:%s@sentry.io/%s' % (env['SENTRY_USERNAME'], env['SENTRY_PASSWORD'], env['SENTRY_APPID']),
    'processors': ('raven.processors.Processor',)
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# The system sends out system-related emails to these addresses.
ADMINS = MANAGERS = (
   ('System', 'system@armada.nu'),
)

