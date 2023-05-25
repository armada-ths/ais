"""
This is the settings file to be used on a local development machine.
It's less secure than the production setup but requires less setup
and is generally easier to work with.
"""

from ais.common.settings import *

# Debug mode gives us helpful error messages when a server error
# occurs. This is a serious security flaw if used in production!

DEBUG = True

# This lets us access AIS via its IP address (usually 127.0.0.1),
# which you can't do in production for security reasons.
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = "ais.local.urls"

# Stripe test keys
STRIPE_SECRET = "sk_test_l4sPsGIoc2f8sD5N4D2fZkBY"
STRIPE_PUBLISHABLE = "pk_test_IzgUj9oJhednbt4EIf78esBE"

# Always use the same secret key so we can resume sessions after
# restarting the server. Again, this is a serious security flaw
# if used in production!
SECRET_KEY = "..............¯\_(ツ)_/¯..............."

# todo: Remove after setting production environment in production (2023)
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
