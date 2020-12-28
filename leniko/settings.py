"""
Django settings for leniko project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from distutils.util import strtobool
from dotenv import load_dotenv, find_dotenv

from django.utils.crypto import get_random_string

#-------------------------------------------------------------------------------
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#-------------------------------------------------------------------------------
# Load environment variables
dotenv_path = os.path.join(BASE_DIR, '.env')
if not os.path.isfile(dotenv_path):
	print(f"[ERROR]: '{dotenv_path}' is missing!")

	txt  = f"DJANGO_SECRET_KEY={get_random_string()}\n"
	txt += f"DJANGO_DEBUG=False\n"

	f = open(dotenv_path, "w")
	f.write(txt)
	f.close()

	print(f"[LOG  ]: Created '{dotenv_path}'!")
load_dotenv(dotenv_path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if SECRET_KEY is None:
	print("Food has no salt!")
	exit()


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', "False")
DEBUG = bool(strtobool(DEBUG))

ALLOWED_HOSTS = []
if DEBUG is False:
	ALLOWED_HOSTS = [
		"leniko.gr",
		"lenikojewelry.gr",
		"lenikojewelry.com",
		"tedicreations.pythonanywhere.com"
	]

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',

	'sorl.thumbnail',

	'pages',
	'products'
]

if DEBUG is True:
	INSTALLED_APPS.append('django.contrib.staticfiles')

if DEBUG is True:
	INSTALLED_APPS.append('debug_toolbar')


MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG is True:
	MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'leniko.urls'

LOGIN_URL = '/login'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'leniko.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# User uploaded files
MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INTERNAL_IPS = []

if DEBUG is True:
	INTERNAL_IPS.append('127.0.0.1')

	DEBUG_TOOLBAR_PANELS = [
		'debug_toolbar.panels.versions.VersionsPanel',
		'debug_toolbar.panels.timer.TimerPanel',
		'debug_toolbar.panels.settings.SettingsPanel',
		'debug_toolbar.panels.headers.HeadersPanel',
		'debug_toolbar.panels.request.RequestPanel',
		'debug_toolbar.panels.sql.SQLPanel',
		'debug_toolbar.panels.staticfiles.StaticFilesPanel',
		'debug_toolbar.panels.templates.TemplatesPanel',
		'debug_toolbar.panels.cache.CachePanel',
		'debug_toolbar.panels.signals.SignalsPanel',
		'debug_toolbar.panels.logging.LoggingPanel',
		'debug_toolbar.panels.redirects.RedirectsPanel',
	]
