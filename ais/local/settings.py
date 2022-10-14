"""
This is the settings file to be used on a local development machine.
It's less secure than the production setup but requires less setup
and is generally easier to work with.
"""

import os
from ais.common.settings import *

# Debug mode gives us helpful error messages when a server error
# occurs. This is a serious security flaw if used in production!

DEBUG = True

# This lets us access AIS via its IP address (usually 127.0.0.1),
# which you can't do in production for security reasons.
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ROOT_URLCONF = 'ais.local.urls'

# Use KTH OpenID Connect for authentication
INSTALLED_APPS += ('kth_login', 'raven.contrib.django.raven_compat',)

# Stripe test keys
STRIPE_SECRET = 'sk_test_l4sPsGIoc2f8sD5N4D2fZkBY'
STRIPE_PUBLISHABLE = 'pk_test_IzgUj9oJhednbt4EIf78esBE'

# We don't need performance here so use SQLite for ease of setup.
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DB_NAME', 'ais_dev'),
        'USER': os.environ.get('DB_USER', 'ais_dev'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'ais_dev'),
        # 'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'HOST': 'db',
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

SALES_HOOK_URL = 'https://hooks.slack.com/services/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'
RECRUITMENT_HOOK_URL = 'https://hooks.slack.com/services/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'

# Always use the same secret key so we can resume sessions after
# restarting the server. Again, this is a serious security flaw
# if used in production!
# SECRET_KEY = '..............¯\_(ツ)_/¯...............'
# SECRET_KEY = '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'
# SECRET_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC5s9xs/XUBZUzdA46f2UH+IbRmz3WtZ3GqFBDRoR0QXUysbnvUgi6FKyefQWAGtKvllnfldS7mrjxPKpNXNVlFgLgnki0A+cVzVRbGWHKa5U2DTGPNPcZx7IKhEVWd7LhQo3CqlUmX6aBy9RR9eo4nIJIZ7Y1xBUZ2mSlfqKBY8xIBzDYBhlMw1ztm9gQSAGowmGsFrRN/eCw/sYYybdbHI473FfeuZ9CJrR/RfFo2A+lPv1RmV+0fmVinYsQoLgtr+uW8OOtTIlfYqO7cWk2n8Qm2+H2libLLPKxqUQ4zcs+pD8aufMEUdoJ7iBWuDhV/i12o+JUSjUVB+DMjIm/sbFs+bdYySE6y0sMtc2cTDYIIVpu3IPdPl8SBH1G+FzV4Tg0ydd1qddoPpWiDqRuxt+hrilYy4H9+Ux1lmDmWoekE+EIN0mq70vMCYcp4FVjkvRBO0usvQ2BBU4la3iOqHyHZpGCqXfBluB0Xrt2eRll+scrMODqAPJRH7rywhpE= arrade@Antons-MacBook-Pro.local'
SECRET_KEY = 'secret'

# This is for AUTHLIB package for interacting with KTH OpenID Connect
# APPLICATION_ID is given from the 'secrets.py' file.
# CLIENT_SECRET is given from the 'secrets.py' file.
AUTHLIB_OAUTH_CLIENTS = {
    'kth': {
        'client_id': os.environ.get('APPLICATION_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'api_base_url': 'https://login.ug.kth.se/adfs/oauth2/',
    }
}
LOGOUT_REDIRECT_URL = '/'

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
AWS_STORAGE_BUCKET_NAME='armada-ais-files'
