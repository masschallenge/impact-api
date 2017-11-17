# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import os

from configurations import Configuration, values
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

    DATABASES = values.DatabaseURLValue()

    DATABASE_ROUTERS = ['impact.routers.APIRouter']

    EMAIL = values.EmailURLValue()

    SECRET_KEY = values.Value()

    SITE_ID = 1

    ROOT_URLCONF = 'impact.urls'

    WSGI_APPLICATION = 'impact.wsgi.application'

    INSTALLED_APPS = [
        'accelerator.apps.AcceleratorConfig',
        'corsheaders',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.staticfiles',
        'embed_video',
        'impact',
        'oauth2_provider',
        'rest_framework',
        'rest_framework.authtoken',
        'rest_framework_sso',
        'rest_framework_swagger',
        'rest_framework_tracking',
        'simpleuser.apps.SimpleuserConfig',
    ]
    ACCELERATOR_MODELS_ARE_MANAGED = False

    AUTH_USER_MODEL = 'simpleuser.User'

    MIDDLEWARE_CLASSES = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
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

    CORS_ORIGIN_ALLOW_ALL = True
    # settings.py
    REST_PROXY = {
        'HOST': bytes(
            os.environ.get('ACCELERATE_SITE_URL',
                           'https://accelerate.masschallenge.org'), 'utf-8'),
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
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    }

    AUTHENTICATION_BACKENDS = (
        'oauth2_provider.backends.OAuth2Backend',
        'simpleuser.email_model_backend.EmailModelBackend',
        'django.contrib.auth.backends.ModelBackend',
    )


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
    TEST_RUNNER = 'impact.test_runner.UnManagedModelTestRunner'
    LANGUAGE_CODE = 'en'


class Prod(Base):
    ALLOWED_HOSTS = Base.ALLOWED_HOSTS + [
        os.environ.get('DJANGO_ALLOWED_HOST', '*'),
    ]
