"""
This is the settings file containing settings common to both the
development and production environments.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os import path

BASE_DIR = path.join(path.dirname(path.abspath(__file__)), "../../")

CRISPY_TEMPLATE_PACK = "bootstrap3"

INSTALLED_APPS = (
    "whitenoise.runserver_nostatic",
    "magic_link",
    "dal",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "hijack",
    "hijack.contrib.admin",
    "corsheaders",
    "webpack_loader",
    "polymorphic",
    "events",
    "companies",
    "fair",
    "people",
    "locations",
    "recruitment",
    "api",
    "news",
    "orders",
    "unirel",
    "crispy_forms",
    "exhibitors",
    "django.contrib.humanize",
    "banquet",
    "register",
    "matching",
    "student_profiles",
    "transportation",
    "accounting",
    "dynamic_formsets",
    "journal",
    "markupfield",
    "testpage",
    "kth_login",
    "raven.contrib.django.raven_compat",
    "rest_framework",
)

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "hijack.middleware.HijackUserMiddleware",
    "recruitment.middleware.LoginRequiredMiddleware",
]

USE_ETAGS = True

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("DB_NAME", "ais_dev"),
        "USER": os.environ.get("DB_USER", "ais_dev"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "ais_dev"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 600,
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "bundles/",
        "STATS_FILE": path.join(BASE_DIR, "webpack-stats.js"),
    }
}

WSGI_APPLICATION = "ais.wsgi.application"

STATIC_ROOT = path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = (path.join(BASE_DIR, "ais_static"),)

ADMIN_MEDIA_PREFIX = "/static/admin/"
MEDIA_ROOT = path.abspath(path.join(BASE_DIR, "..", "media"))

MEDIA_URL = "/media/"

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Stockholm"
USE_I18N = True
LANGUAGE_CODE = "en-us"
USE_L10N = False
DATE_FORMAT = "M j, Y"
DATETIME_FORMAT = "M j, Y, H:i"

# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = "noreply@armada.nu"
DEFAULT_TO_EMAIL = "info@armada.nu"
EMAIL_HOST_USER = "noreply@armada.nu"
EMAIL_HOST_PASSWORD = os.environ.get("DUMMY", "dummy")
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SALES_HOOK_URL = (
    "https://hooks.slack.com/services/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"
)
RECRUITMENT_HOOK_URL = (
    "https://hooks.slack.com/services/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"
)

# This is for AUTHLIB package for interacting with KTH OpenID Connect
# APPLICATION_ID is given from the 'secrets.py' file.
# CLIENT_SECRET is given from the 'secrets.py' file.
AUTHLIB_OAUTH_CLIENTS = {
    "kth": {
        "client_id": os.environ.get("APPLICATION_ID"),
        "client_secret": os.environ.get("CLIENT_SECRET"),
        "api_base_url": "https://login.ug.kth.se/adfs/oauth2/",
    }
}
LOGOUT_REDIRECT_URL = "/"

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
AWS_STORAGE_BUCKET_NAME = "armada-ais-files"
