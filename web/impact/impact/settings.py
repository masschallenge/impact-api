# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import os
import logging
import datetime
from configurations import (
    Configuration,
    values,
)
from django.urls import reverse_lazy
from unipath import Path


class Base(Configuration):
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'America/New_York'

    LOGIN_URL = reverse_lazy('auth_login')
    LOGIN_REDIRECT_URL = reverse_lazy('api-root')
    LOGOUT_REDIRECT_URL = reverse_lazy('auth_login')

    ADMINS = (
    )

    MANAGERS = ADMINS

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    USE_X_FORWARDED_HOST = True

    ALLOWED_HOSTS = [
        '*'
    ]

    PROJECT_DIR = Path(__file__).ancestor(2)

    LOCALE_PATH = PROJECT_DIR.child('locale')

    STATIC_ROOT = PROJECT_DIR.child('static-compiled')

    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        PROJECT_DIR.child('static')
    ]

    MEDIA_ROOT = PROJECT_DIR.child('media')

    MEDIA_URL = '/media/'

    DATABASES = values.DatabaseURLValue().value

    SLAVE_DATABASES = ['default']

    if os.environ.get('READ_REPLICA_DATABASE_URL'):
        DATABASES.update(values.DatabaseURLValue(  # pragma: no cover
            alias='read-replica',
            environ_name='READ_REPLICA_DATABASE_URL').value)

        SLAVE_DATABASES = ['read-replica']  # pragma: no cover

        DATABASE_ROUTERS = ('multidb.MasterSlaveRouter',)  # pragma: no cover

    EMAIL = values.EmailURLValue()

    SECRET_KEY = values.Value()

    SITE_ID = 1

    ROOT_URLCONF = 'impact.urls'

    WSGI_APPLICATION = 'impact.wsgi.application'

    INSTALLED_APPS = [
        'paypal.standard',
        'paypal.pro',
        'paypal.standard.pdt',
        'accelerator',
        'simpleuser',
        'corsheaders',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.staticfiles',
        'sorl.thumbnail',
        'embed_video',
        'oauth2_provider',
        'rest_framework',
        'rest_framework.authtoken',
        'oidc_provider',
        'rest_framework_swagger',
        'fluent_pages',
        'impact',
        'graphene_django',
        'sitetree',
    ]

    ACCELERATOR_MODELS_ARE_MANAGED = True

    AUTH_USER_MODEL = 'simpleuser.User'

    MIDDLEWARE_CLASSES = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'impact.graphql.auth.middleware.CookieJSONWebTokenMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.admindocs.middleware.XViewMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'oauth2_provider.middleware.OAuth2TokenMiddleware',
        'impact.middleware.MethodOverrideMiddleware',
    ]

    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': os.environ['DJANGO_HIREDIS_CACHE_LOCATION'],
            'OPTIONS': {
                'DB': 1,
                'PARSER_CLASS': 'redis.connection.HiredisParser',
            }
        },
    }

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [PROJECT_DIR.child('templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.csrf'
                ],
            },
        },
    ]
    OIDC_USERINFO = 'impact.oidc_provider_settings.userinfo'
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = (
        'localhost:1234',
        'localhost:8000',
        'localhost:8181',
    )
    CORS_ORIGIN_REGEX_WHITELIST = (
        r'^(https?://)?(\w+\.)?masschallenge\.org$', )
    ALGOLIA_INDEX_PREFIX = os.environ.get('ALGOLIA_INDEX_PREFIX', 'dev')
    ALGOLIA_INDEXES = [
        '{algolia_prefix}_mentor'.format(algolia_prefix=ALGOLIA_INDEX_PREFIX)
    ]
    NEW_RELIC_CONFIG_FILE = os.path.join(PROJECT_DIR, 'newrelic.ini')
    NEW_RELIC_ENVIRONMENT = os.environ.get('NEW_RELIC_ENVIRONMENT',
                                           'development')

    ALGOLIA_APPLICATION_ID = os.environ.get('ALGOLIA_APPLICATION_ID', '')

    ALGOLIA_API_KEY = os.environ.get('ALGOLIA_API_KEY', '')

    ALGOLIA_STAFF_SEARCH_ONLY_API_KEY = os.environ.get(
        'ALGOLIA_STAFF_SEARCH_ONLY_API_KEY', '')

    ALGOLIA_SEARCH_ONLY_API_KEY = os.environ.get(
        'ALGOLIA_SEARCH_ONLY_API_KEY', '')

    V0_SECURITY_KEY = bytes(
        os.environ.get('IMPACT_API_V0_SECURITY_KEY', 'XXX'),
        'utf-8')

    V0_IMAGE_PASSWORD = bytes(
        os.environ.get('IMPACT_API_V0_IMAGE_PASSWORD', 'XXX'),
        'utf-8')

    V0_SITE_NAME = bytes(os.environ.get(
        'IMPACT_API_V0_SITE_NAME', 'masschallenge.org'), 'utf-8')

    V0_API_GROUP = bytes(os.environ.get(
        'IMPACT_API_V0_API_GROUP', 'v0_clients'), 'utf-8')

    # This and the above should get generalized.  See AC-4574.
    V1_API_GROUP = bytes(os.environ.get(
        'IMPACT_API_V1_API_GROUP', 'v1_clients'), 'utf-8')

    V1_CONFIDENTIAL_API_GROUP = bytes('v1_confidential', 'utf-8')

    OAUTH2_PROVIDER = {
        # this is the list of available scopes
        'SCOPES': {
            'read': 'Read scope',
            'write': 'Write scope',
            'groups': 'Access to your groups'
        }
    }

    # settings.py
    REST_PROXY = {
        'HOST': os.environ.get('ACCELERATE_SITE_URL',
                               'https://accelerate.masschallenge.org'),
        'AUTH': {
            'user': None,
            'password': None,
            # Or alternatively:
            'token': None,
        },
        'VERIFY_SSL': False,
    }

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': (
            'rest_framework.pagination.LimitOffsetPagination'),
        'PAGE_SIZE': 10,
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    }

    AUTHENTICATION_BACKENDS = (
        'oauth2_provider.backends.OAuth2Backend',
        'impact.graphql.auth.authentication_backend.JWTokenCookieBackend',
        'simpleuser.email_model_backend.EmailModelBackend',
        'django.contrib.auth.backends.ModelBackend',
    )
    SESSION_COOKIE_AGE = 3600 * 24 * 7 * 2  # default
    JWT_AUTH = {
        'JWT_ALLOW_REFRESH': False,
        'JWT_EXPIRATION_DELTA': datetime.timedelta(
            seconds=(SESSION_COOKIE_AGE * 2)),
        # after timedelta has passed, token is no longer valid, and cannot
        # be refreshed any longer
        'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(
            seconds=(SESSION_COOKIE_AGE * 2)),
        # after timedelta has passed since first obtaining the token,
        # it is no longer possible to refresh the token, even if the token
        # did not expire
        'JWT_AUTH_COOKIE': os.environ.get('JWT_AUTH_COOKIE', ''),
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY', ''),
        'FIRST_NAME_KEY': 'first_name',
    }

    PAYPAL_WPP_USER = ''
    PAYPAL_WPP_PASSWORD = ''
    PAYPAL_WPP_SIGNATURE = ''
    PAYPAL_RECEIVER_EMAIL = ''
    PAYPAL_IDENTITY_TOKEN = ''

    MPTT_SWAPPABLE_INDUSTRY_MODEL = "accelerator.Industry"
    MPTT_SWAPPABLE_INDUSTRY_MODEL_ADDITIONAL = "accelerator.Industry"
    MPTT_SWAPPABLE_INDUSTRY_DB_TABLE_NAME = (
        "accelerator_startup_related_industry")
    MPTT_SWAPPABLE_FUNCTIONALEXPERTISE_MODEL = (
        "accelerator.FunctionalExpertise")

    CMS_FILE_ROOT = '/var/www/cms-files'

    IMAGE_RESIZE_HOST = "https://dl4fx6jt7wkin.cloudfront.net"
    IMAGE_RESIZE_TEMPLATE = "/fit-in/500x500/media/{}"


class Dev(Base):
    DEBUG = True

    Base.TEMPLATES[0]['OPTIONS']['debug'] = True

    INTERNAL_IPS = (
        '127.0.0.1',
    )

    ALLOWED_HOSTS = [
        '*'
    ]

    MIDDLEWARE_CLASSES = [
                             'debug_toolbar.middleware.DebugToolbarMiddleware',
                         ] + Base.MIDDLEWARE_CLASSES

    INSTALLED_APPS = Base.INSTALLED_APPS + [
        'debug_toolbar',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda x: True
    }


class Test(Base):
    MIGRATION_MODULES = {'django.contrib.auth': None, 'impact': None}
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'HOST': '',
            'NAME': 'test.db',
            'USER': '',
            'PASSWORD': ''
        }
    }
    DATABASE_ROUTERS = []
    DEBUG = False
    LANGUAGE_CODE = 'en'

    logging.disable(logging.CRITICAL)


class Prod(Base):
    ALLOWED_HOSTS = Base.ALLOWED_HOSTS + [
        os.environ.get('DJANGO_ALLOWED_HOST', '*'),
    ]

    AWS_LOCATION = 'media'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    MEDIA_ROOT = AWS_LOCATION

    DEFAULT_FILE_STORAGE = 'impact.media_storage_backend.MediaStorageBackend'
    STATICFILES_STORAGE = (
        'django.contrib.staticfiles.storage.StaticFilesStorage')
