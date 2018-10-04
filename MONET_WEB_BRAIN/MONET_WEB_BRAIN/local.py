from .base import *

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'monet',
        'USER': 'monet_user',
        'PASSWORD': 'monet1234',
        'HOST': 'localhost',
        'PORT': '',
    }
}
