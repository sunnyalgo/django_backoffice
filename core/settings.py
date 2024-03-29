"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-95n6@52(f^__n8opfsdfcmoqyv8*eaxh#&iwun06ne!d8%$7fb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'TRUE'

# Celery
_BROKER_USER = os.environ.get('BROKER_USER', 'guest')
_BROKER_PASSWORD = os.environ.get('BROKER_PASSWORD', 'guest')
_BROKER_HOST = os.environ.get('BROKER_HOST', 'localhost')
_BROKER_PORT = os.environ.get('BROKER_PORT', 5672)
_BROKER_VHOST = os.environ.get('BROKER_VHOST', '/')
BROKER_URL = f'amqp://{_BROKER_USER}:{_BROKER_PASSWORD}@{_BROKER_HOST}:{_BROKER_PORT}/{_BROKER_VHOST}'
CELERY_ALWAYS_EAGER = False
CELERY_RESULT_BACKEND = 'disabled'

if not DEBUG:
    ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]']

# Application definition
INSTALLED_APPS = [
    'django_extensions',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.customer',
    'apps.financial',
    'apps.product',
    'apps.sales',
    'apps.tasks_pipeline',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DATABASE_NAME', 'django_backoffice'),
        'USER': os.environ.get('DATABASE_USER', 'django_backoffice'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'django_backoffice'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Media URL files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
PACKING_SLIP_FOLDER = 'pdf/packing_slip'
PACKING_SLIP_ROOT = MEDIA_ROOT / PACKING_SLIP_FOLDER

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
