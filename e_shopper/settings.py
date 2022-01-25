from pathlib import Path
from .security_settings import *

from os import path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = project_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.discord',
    'ckeditor',
    'ckeditor_uploader',
    'debug_toolbar',
    'mptt',
    'rest_framework',
    'snowpenguin.django.recaptcha3',

    'Blog',
    'Interactive',
    'Shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'e_shopper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'e_shopper.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L10N = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = mail_host
EMAIL_PORT = mail_port
EMAIL_HOST_USER = mail_host_user
EMAIL_HOST_PASSWORD = mail_host_pass
EMAIL_USE_TLS = mail_TLS
EMAIL_USE_SSL = mail_SSL

DEFAULT_FROM_EMAIL = mail_host_user
SERVER_EMAIL = mail_host_user
RECIPIENTS_EMAIL = [mail_host_user]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# LOGIN_URL = 'registration/login/'

STATIC_URL = '/static/'
STATIC_DIR = path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
# STATIC_ROOT = path.join(BASE_DIR, 'static')

CKEDITOR_UPLOAD_PATH = "uploads/"

MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media')

LOCALE_PATHS = (path.join(BASE_DIR, 'locale'),)

LANGUAGES = (
    ('ru', 'Russia'),
    ('en', 'English'),
    ('de', 'German'),
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = ['127.0.0.1', 'localhost']

RECAPTCHA_PUBLIC_KEY = PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = PRIVATE_KEY
RECAPTCHA_DEFAULT_ACTION = DEFAULT_ACTION
RECAPTCHA_SCORE_THRESHOLD = SCORE_THRESHOLD
RECAPTCHA_LANGUAGE = 'en'

SITE_ID = 1

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 4
ACCOUNT_USERNAME_MIN_LENGTH = 4
