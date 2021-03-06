import os

from django.utils.crypto import get_random_string

from configparser import ConfigParser


# ------------------------------------------------------------------------------
# Project absolute directory

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ------------------------------------------------------------------------------
# Load environment variables

def envconfig(key, default=None):
	"""Help function for retrieving configs"""

	envfile = '.env'

	config = ConfigParser()
	config.optionxform = str
	config.read(envfile)

	v = None
	try:
		v = config['DEFAULT'][key]
	except KeyError:
		if default is not None:
			config['DEFAULT'][key] = str(default)
			with open(envfile, 'w') as configfile:
				config.write(configfile)
			v = default
			print(f"\u001b[32m{key} is configured!\u001b[0m")
		else:
			print(f"\u001b[31m{key} is not configured!\u001b[0m")
			exit()

	with open(envfile, 'w') as configfile:
		config.write(configfile)

	if v is None:
		raise Exception("\u001b[31menvconfig failed!\u001b[0m")
	return v


# ------------------------------------------------------------------------------
# Secret key

SECRET_KEY = envconfig("SECRET_KEY", get_random_string())

# ------------------------------------------------------------------------------
# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',

	'pages',
	'products',
	'cart'
]

# ------------------------------------------------------------------------------
# Redis

REDIS_LOCATION = envconfig('REDIS_LOCATION', "redis://127.0.0.1:6379/1")
REDIS_HOSTNAME = envconfig('REDIS_HOSTNAME', "127.0.0.1")
REDIS_PORT = int(envconfig('REDIS_PORT', "6379"))
REDIS_PASSWORD = envconfig('REDIS_PASSWORD', "")

# ------------------------------------------------------------------------------
# Cache

"""
CACHES = {
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": REDIS_LOCATION,
		"OPTIONS": {
			"PASSWORD": REDIS_PASSWORD,
			"CLIENT_CLASS": "django_redis.client.DefaultClient"
		},
		"KEY_PREFIX": "example"
	}
}
"""

# ------------------------------------------------------------------------------
# Thumbnails

# THUMBNAIL_BACKEND = 'sorl.thumbnail.base.ThumbnailBackend'
THUMBNAIL_BACKEND = 'products.internal.utils.MyThumbnailBackend'
INSTALLED_APPS.append('sorl.thumbnail')

THUMBNAIL_REDIS_HOST = REDIS_HOSTNAME
THUMBNAIL_REDIS_PORT = REDIS_PORT
THUMBNAIL_REDIS_PASSWORD = REDIS_PASSWORD
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

# ------------------------------------------------------------------------------
# Middleware

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------------------------------------
# URLS

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


# ------------------------------------------------------------------------------
# Database

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}


# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ------------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# ------------------------------------------------------------------------------
# User uploaded files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ------------------------------------------------------------------------------
# Filestorage

# Dropbox
"""
INSTALLED_APPS.append('storages')
DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'

DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN', '')
if DROPBOX_OAUTH2_TOKEN == '':
	print(f"Forgot dropbox token!")
	exit()
"""
