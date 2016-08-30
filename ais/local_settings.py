"""
This is the settings file to be used on a local development machine.
It's less secure than the production setup but requires less setup
and is generally easier to work with.
"""

import os
from ais.common_settings import *

# Debug mode gives us helpful error messages when a server error
# occurs. This is a serious security flaw if used in production!
DEBUG = True

# This lets us access AIS via its IP address (usually 127.0.0.1),
# which you can't do in production for security reasons. 
ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'example_urls'

# We don't need performance here so use SQLite for ease of setup.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Always use the same secret key so we can resume sessions after
# restarting the server. Again, this is a serious security flaw
# if used in production!
SECRET_KEY = '..............¯\_(ツ)_/¯...............'

