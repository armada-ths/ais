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
# The URL scheme is slightly different in a development environment
# since there's no CAS integration.
ROOT_URLCONF = 'ais.local.urls'

# We don't need performance here so use SQLite for ease of setup.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


SALES_HOOK_URL = 'https://hooks.slack.com/services/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'
RECRUITMENT_HOOK_URL = 'https://hooks.slack.com/services/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'

# Always use the same secret key so we can resume sessions after
# restarting the server. Again, this is a serious security flaw
# if used in production!
SECRET_KEY = '..............¯\_(ツ)_/¯...............'

