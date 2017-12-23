"""
This is the settings file to be used in a production environment. It's
more secure, more robust and more performant than the development setup
and also configures AIS to talk to external services (e.g. CAS).
"""

import os
from os import environ as env
from os import path
import saml2
from ais.common.settings import *
from ais.secrets import *

# This is important so other people can't set their own domains
# to point to AIS (which would be a security concern).
ALLOWED_HOSTS = ['.armada.nu', 'localhost']

# The URL scheme is slightly different in a production environment
# since we need to accomodate the CAS integration.
ROOT_URLCONF = 'ais.production.urls'

# Use KTH CAS for authentication
#INSTALLED_APPS += ('cas', 'raven.contrib.django.raven_compat',)
#AUTHENTICATION_BACKENDS += ('cas.backends.CASBackend',)
#CAS_SERVER_URL = 'https://login.kth.se/'
#CAS_AUTO_CREATE_USER = False
#CAS_RESPONSE_CALLBACKS = ('lib.CAS_callback.callback',)

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

# SAML settings
# followed documentation that exists
# in html file in /docs/saml_html_files/
BASEDIR = path.dirname(path.abspath(__file__))
SAML_CONFIG = {
  # full path to the xmlsec1 binary programm
  'xmlsec_binary': '/usr/bin/xmlsec1',

  # your entity id, usually your subdomain plus the url to the metadata view
  'entityid': 'https://armada.nu/saml2/metadata/',

  # directory with attribute mapping
  'attribute_map_dir': path.join(BASEDIR, '../../attribute-maps'),

  # this block states what services we provide
  'service': {
      # we are just a lonely SP
      'sp' : {
          'name': 'THS Armada',
          'endpoints': {
              # url and binding to the assetion consumer service view
              # do not change the binding or service name
              'assertion_consumer_service': [
                  ('https://armada.nu/saml2/acs/',
                   saml2.BINDING_HTTP_POST),
                  ],
              # url and binding to the single logout service view
              # do not change the binding or service name
              'single_logout_service': [
                  [('https://armada.nu/saml2/ls/',
                   saml2.BINDING_HTTP_REDIRECT),
                  ],
                  [('https://armada.nu/saml2/ls/post',
                   saml2.BINDING_HTTP_POST),
                  ]
                 ]
              },

           # attributes that this project need to identify a user
          'required_attributes': ['uid'],

           # attributes that may be useful to have but not required
          'optional_attributes': ['eduPersonAffiliation'],

          # in this section the list of IdPs we talk to are defined
          'idp': {
              # we do not need a WAYF service since there is
              # only an IdP defined here. This IdP should be
              # present in our metadata

              # the keys of this dictionary are entity ids
              'https://localhost/simplesaml/saml2/idp/metadata.php': {
                  'single_sign_on_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://saml.sys.kth.se/idp/shibboleth',
                      },
                  'single_logout_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://saml.sys.kth.se/idp/shibboleth',
                      },
                  },
              },
          },
      },

  # where the remote metadata is stored
  'metadata': {
      'local': [path.join(BASEDIR, '../../swamid_metadata.xml')],
      },

  # set to 1 to output debugging information
  'debug': 1,

  # certificate
  'key_file': path.join(BASEDIR, '../../private/mycert.key'),  # private part
  'cert_file': path.join(BASEDIR, '../../private/mycert.pem'),  # public part

  # own metadata settings
  'contact_person': [
      {'given_name': 'Project Manager',
       'sur_name': 'Armada',
       'company': 'Armada',
       'email_address': 'system@armada.nu',
       'contact_type': 'project manager'},
      ],
  # you can set multilanguage information here
  'organization': {
      'name': [('THS Armada', 'en')],
      'display_name': [('THS Armada', 'en')],
      'url': [('https://armada.nu', 'en')],
      }
 }
