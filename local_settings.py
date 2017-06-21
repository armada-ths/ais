from ais.local.settings import *

#MEDIA_ROOT = '/vagrant/media'
#MEDIA_URL = '/media/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
