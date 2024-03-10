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
    "http://localhost:8000",
    "http://localhost:4321",  # For astro site
    "https://armada-nu.pages.dev",  # Temporary deployment
]

CORS_ALLOWED_ORIGINS_REGEXES = ["^https:\/\/\w+--armada\.netlify\.app$"]

DEBUG = False

# The URL scheme is slightly different in a production environment
# since we need to accomodate the KTH OpenID Connect integration.
ROOT_URLCONF = "ais.production.urls"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_QUERYSTRING_EXPIRE = 60 * 60 * 24 * 7  # 1 week

STRIPE_SECRET = os.environ.get("STRIPE_SECRET")
STRIPE_PUBLISHABLE = os.environ.get("STRIPE_PUBLISHABLE")

# The system sends out system-related emails to these addresses.
# ADMINS = MANAGERS = (("System", "system@armada.nu"),)
ADMINS = MANAGERS = ()
