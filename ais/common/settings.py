"""
This is the settings file containing settings common to both the
development and production environments.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os import path

BASE_DIR = path.join(path.dirname(path.abspath(__file__)), '../../')

# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'info@armada.nu'
DEFAULT_TO_EMAIL = 'info@armada.nu'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

INSTALLED_APPS = (
    'root',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpack_loader',
    'polymorphic',
    'events',
    'companies',
    'fair',
    'people',
    'locations',
    'recruitment',
    'api',
    'news',
    'orders',
    'crispy_forms',
    'exhibitors',
    'django.contrib.humanize',
    'banquet',
    'register',
    'matching',
    'student_profiles',
    'transportation',
    'accounting',
    'dynamic_formsets',
    'journal',
    'markupfield',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'recruitment.middleware.LoginRequiredMiddleware'
)

USE_ETAGS = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': path.join(BASE_DIR, 'webpack-stats.js')
    }
}

WSGI_APPLICATION = 'ais.wsgi.application'

STATIC_ROOT = path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    path.join(BASE_DIR, "ais_static"),
)

ADMIN_MEDIA_PREFIX = '/static/admin/'
MEDIA_ROOT = path.abspath(path.join(BASE_DIR, '..', 'media'))

MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Stockholm'
USE_I18N = True
USE_TZ = True
LANGUAGE_CODE = 'en-us'
USE_L10N = False
DATE_FORMAT = "M j, Y"
DATETIME_FORMAT = "M j, Y, H:i"
