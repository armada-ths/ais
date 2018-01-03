"""
This is the settings file to be used on a local development machine.
It's less secure than the production setup but requires less setup
and is generally easier to work with.
"""

import os
from os import path
import saml2
import saml2.saml
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


# local PYSAML settings (see html file in /docs/saml_html_files)
BASEDIR = path.dirname(path.abspath(__file__))
SAML_CONFIG = {
  # full path to the xmlsec1 binary programm
  'xmlsec_binary': '/usr/local/bin/xmlsec1',

  # your entity id, usually your subdomain plus the url to the metadata view
  'entityid': 'http://localhost:8000/saml2/metadata/',

  # directory with attribute mapping
  'attribute_map_dir': path.join(BASEDIR, '../../attribute-maps'),

  # this block states what services we provide
  'service': {
      # we are just a lonely SP
      'sp' : {
          'name': 'THS Armada',
          'name_id_format': saml2.saml.NAMEID_FORMAT_PERSISTENT,
          'endpoints': {
            # url and binding to the assetion consumer service view
            # do not change the binding or service name
            'assertion_consumer_service': [
                ('http://localhost:8000/saml2/acs/', saml2.BINDING_HTTP_POST),
            ],
            # url and binding to the single logout service view
            # do not change the binding or service name
            'single_logout_service': [
                ('http://localhost:8000/saml2/ls/', saml2.BINDING_HTTP_REDIRECT),
                ('http://localhost:8000/saml2/ls/post', saml2.BINDING_HTTP_POST),
            ],
          },

           # attributes that this project need to identify a user
          'required_attributes': ['uid', 'mail', 'displayName'],

           # attributes that may be useful to have but not required
          'optional_attributes': ['eduPersonAffiliation'],

          # in this section the list of IdPs we talk to are defined
          'idp': {
              # we do not need a WAYF service since there is
              # only an IdP defined here. This IdP should be
              # present in our metadata

              # the keys of this dictionary are entity ids
              'https://stubidp.sustainsys.com/Metadata': {
                  'single_sign_on_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://stubidp.sustainsys.com/',
                      },
                  'single_logout_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://stubidp.sustainsys.com/Logout',
                      },
                  },
              },
          },
      },

  # where the remote metadata is stored
  'metadata': {
      'local': [path.join(BASEDIR, '../../remote_metadata.xml')],
      },

  # set to 1 to output debugging information
  'debug': 1,

  # certificate
  'key_file': path.join(BASEDIR, '../../private/mycert.key'),  # private part
  'cert_file': path.join(BASEDIR, '../../private/mycert.pem'),  # public part

  # own metadata settings
  'contact_person': [
      {'given_name': 'System Manager',
       'sur_name': 'THS Armada',
       'company': 'THS Armada',
       'email_address': 'system@armada.nu',
       'contact_type': 'system manager'},
      ],
  # you can set multilanguage information here
  'organization': {
      'name': [('THS Armada', 'en')],
      'display_name': [('THS Armada', 'en')],
      'url': [('https://armada.nu', 'en')],
      }
 }
