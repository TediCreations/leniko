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
	'django.contrib.messages'
]

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
# Templates

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
# My apps

INSTALLED_APPS.append('pages')
INSTALLED_APPS.append('dev')
INSTALLED_APPS.append('products')
INSTALLED_APPS.append('cart')
INSTALLED_APPS.append('checkout')

# ------------------------------------------------------------------------------
# Redis

REDIS_LOCATION = envconfig('REDIS_LOCATION', "redis://127.0.0.1:6379/1")
REDIS_HOSTNAME = envconfig('REDIS_HOSTNAME', "127.0.0.1")
REDIS_PORT = int(envconfig('REDIS_PORT', "6379"))
REDIS_PASSWORD = envconfig('REDIS_PASSWORD', "")

# ------------------------------------------------------------------------------
# Constance

INSTALLED_APPS.append('constance')

CONSTANCE_ADDITIONAL_FIELDS = {
	'yes_no_null_select': [
		'django.forms.fields.ChoiceField',
		{
			'widget': 'django.forms.Select',
			'choices': ((None, "-----"), ("yes", "Yes"), ("no", "No"))
		}
	],
	'email': ('django.forms.fields.EmailField',),
	'time': ('django.forms.fields.TimeField',)
}

CONSTANCE_CONFIG = {

	# 'SITE_NAME': ('Leniko Jewelry', 'Website title', str),
	# 'SITE_DESCRIPTION': ('Handmade Jewelry design', 'Website description', str),
	'SITE_THEME': ('leniko', 'Website theme', str),
	'SITE_URL': ('https://dev.leniko.gr', 'Website theme', str),

	# Contact
	'EMAIL': ('support@leniko.gr', 'Website email', 'email'),
	'PHONE': ('6979321203', 'Phone number', str),
	'ADDRESS': ('Patriarxou Ioakeim 10', 'Address', str),
	'COUNTRY': ('Greece', 'Country', str),
	'CITY': ('Thessaloniki', 'City', str),
	'POSTAL_CODE': ('54622', 'Postal code', str),

	# Website messages
	'TOPBAR_MESSAGE': ('Welcome to leniko shop', 'Topbar message', str),
	'CART_MESSAGE': ('Thank you for shopping with us!', 'Cart message', str),

	# Functionality
	'IS_CUSTOMER_LOGIN': (False, 'Customer login system', bool),
	'IS_WISHLIST': (False, 'Wishlist system', bool),
	'IS_CART': (True, 'Cart system', bool),
	'IS_ORDERS': (True, 'Order system', bool),

	# Shop information
	'HOUR_OF_OPERATION': ("Monday – Friday : 09:00 – 20:00\n<br>\nSaturday: 10:30 – 15:00\n<br>\nSunday: Closed", 'Monday', str),
	'ORDER_DELIVERY_DAYS': (5, 'How many working days for shipping?', int),
}

CONSTANCE_CONFIG_FIELDSETS = {

	'General Options': {
		'fields': ('SITE_URL', 'SITE_THEME',),  # 'SITE_NAME', 'SITE_DESCRIPTION'
		'collapse': True
	},

	'Contact': {
		'fields': (
			'EMAIL', 'PHONE', 'ADDRESS',
			'COUNTRY', 'CITY', 'POSTAL_CODE'),
		'collapse': True
	},

	'Functionality': {
		'fields': (
			'IS_CUSTOMER_LOGIN', 'IS_WISHLIST',
			'IS_CART', 'IS_ORDERS'),
		'collapse': True
	},

	'Messages': {
		'fields': ('TOPBAR_MESSAGE', 'CART_MESSAGE'),
		'collapse': True
	},

	'Shop info': {
		'fields': (
			'HOUR_OF_OPERATION', 'ORDER_DELIVERY_DAYS'),
		'collapse': True
	}
}

# Database backend
INSTALLED_APPS.append('constance.backends.database')
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

# For the template system
TEMPLATES[0]['OPTIONS']['context_processors'].append('constance.context_processors.config')
# TEMPLATE_CONTEXT_PROCESSORS = (
# 	'constance.context_processors.config',
# )

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
# URLS

ROOT_URLCONF = 'app.urls'

LOGIN_URL = '/login'

WSGI_APPLICATION = 'app.wsgi.application'


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
# Stripe

STRIPE_PUBLIC_KEY = envconfig("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = envconfig("STRIPE_SECRET_KEY")

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
