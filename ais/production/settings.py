"""
This is the settings file to be used in a production environment. It's
more secure, more robust and more performant than the development setup
and also configures AIS to talk to external services.
"""

import os
from ais.common.settings import *

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGINS = [
    "https://armada.nu",
    "https://www.armada.nu",
    "http://armada.nu",
    "http://www.armada.nu",
    "http://localhost:8000"
]

DEBUG = False

# The URL scheme is slightly different in a production environment
# since we need to accomodate the KTH OpenID Connect integration.
ROOT_URLCONF = "ais.production.urls"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# The system sends out system-related emails to these addresses.
ADMINS = MANAGERS = (("System", "system@armada.nu"),)
