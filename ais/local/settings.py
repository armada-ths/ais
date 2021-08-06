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
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ROOT_URLCONF = 'ais.local.urls'

# Use KTH CAS for authentication
INSTALLED_APPS += ('cas', 'raven.contrib.django.raven_compat',)
AUTHENTICATION_BACKENDS += ('cas.backends.CASBackend',)
CAS_SERVER_URL = 'https://login.kth.se/'
CAS_AUTO_CREATE_USER = False
CAS_RESPONSE_CALLBACKS = ('lib.CAS_callback.callback',)

# Stripe test keys
STRIPE_SECRET = 'sk_test_l4sPsGIoc2f8sD5N4D2fZkBY'
STRIPE_PUBLISHABLE = 'pk_test_IzgUj9oJhednbt4EIf78esBE'

# We don't need performance here so use SQLite for ease of setup.
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ais_dev',
        'USER': 'ais_dev',
        'PASSWORD': 'ais_dev',
        # 'HOST': '127.0.0.1',  # Vagrant
        'HOST': 'db',  # Docker
    }
}


SALES_HOOK_URL = 'https://hooks.slack.com/services/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'
RECRUITMENT_HOOK_URL = 'https://hooks.slack.com/services/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'


# Always use the same secret key so we can resume sessions after
# restarting the server. Again, this is a serious security flaw
# if used in production!
SECRET_KEY = '..............¯\_(ツ)_/¯...............'
