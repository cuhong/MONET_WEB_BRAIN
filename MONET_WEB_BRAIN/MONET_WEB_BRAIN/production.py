from .base import *

ALLOWED_HOSTS = ['brain.yonsei.ac.kr']

SECRET_KEY = '1x7w9-)9+tb)ns@az%sng+vl8n132p^w5=qauz#7x@@nvs9(n8'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'monet_web_brain',
        'USER': 'monet_web_brain_user',
        'PASSWORD': 'wkdrhahspdnpq1234',
        'HOST': 'localhost',
        'PORT': '',
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MONET_WEB_BRAIN',
        'USER': 'root',
        'PASSWORD': 'monet1234',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# SSL (HTTPS) SETUP
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_HSTS_SECONDS = 10
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
