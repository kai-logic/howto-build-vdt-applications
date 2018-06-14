"""Settings for Production Server"""
from .base import *
import os
# from django.conf import settings
#
# settings.state = 'prod'
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Enable offline compression
COMPRESS_ENABLED = True

ALLOWED_HOSTS = [
    '*',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        '': {
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        }
    },
}

# HTTPS cookies only in production
HTTPS = os.environ.get('HTTPS', 'true').lower() == 'true'
SESSION_COOKIE_SECURE = HTTPS
CSRF_COOKIE_SECURE = HTTPS
REQUESTS_SESSION_VERIFY_SSL = HTTPS

VSAPI_BASE = os.environ.get('VIDISPINE_URL', 'http://localhost:8080/API/')

# flake8: noqa
