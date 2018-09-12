"""Base settings shared by all environments"""
# Import global settings to make it easier to extend settings.
import os
import sys
import app as project_module
from django.conf.global_settings import *


# ==============================================================================
# Generic Django project settings
# ==============================================================================

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Stockholm'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

DEFAULT_DB_ALIAS = "noDB"

VS_USERNAME = 'admin'
VS_PASSWORD = 'Vidispine1'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'q%yopvowyixb36)=ovnd*ss!%me%nadlb1e-=l^7la$ti^anez'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'webpack_loader',
    'vdt_python_sdk',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
)

SESSION_COOKIE_NAME = 'vsuisession'
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
REQUESTS_SESSION_VERIFY_SSL = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# ==============================================================================
# Calculation of directories relative to the project module location
# ==============================================================================

PROJECT_DIR = os.path.dirname(os.path.realpath(project_module.__file__))

PYTHON_BIN = os.path.dirname(sys.executable)
ve_path = os.path.dirname(os.path.dirname(os.path.dirname(PROJECT_DIR)))
# Assume that the presence of 'activate_this.py' in the python bin/
# directory means that we're running in a virtual environment.
if os.path.exists(os.path.join(PYTHON_BIN, 'activate_this.py')):
    # We're running with a virtualenv python executable.
    VAR_ROOT = os.path.join(os.path.dirname(PYTHON_BIN), 'var')
elif ve_path and os.path.exists(os.path.join(ve_path, 'bin',
                                             'activate_this.py')):
    # We're running in [virtualenv_root]/src/[project_name].
    VAR_ROOT = os.path.join(ve_path, 'var')
else:
    # Set the variable root to a path in the project which is
    # ignored by the repository.
    VAR_ROOT = os.path.join(PROJECT_DIR, 'var')

if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)

# ==============================================================================
# Project URLS and media settings
# ==============================================================================

ROOT_URLCONF = 'app.urls'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'collected_static')
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'dist'),
)

# ==============================================================================
# Templates
# ==============================================================================

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

# TEMPLATE_CONTEXT_PROCESSORS += (
# )

# ==============================================================================
# Middleware
# ==============================================================================

# MIDDLEWARE_CLASSES += (
# )

# ==============================================================================
# Auth / security
# ==============================================================================

AUTHENTICATION_BACKENDS += (
)

# ==============================================================================
# Miscellaneous project settings
# ==============================================================================

# ==============================================================================
# Third party app settings
# ==============================================================================

WEBPACK_LOADER = {
    'DEFAULT': {
            'BUNDLE_DIR_NAME': '/',
            'STATS_FILE': os.path.join(PROJECT_DIR, 'webpack-stats.json'),
        }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, "templates"), ],
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

# flake8: noqa
