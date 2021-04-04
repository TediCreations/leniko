from .base import *

# ------------------------------------------------------------------------------
# Debug
DEBUG = False

# ------------------------------------------------------------------------------
# Hosts

ALLOWED_HOSTS = envconfig("ALLOWED_HOSTS").split()

# ------------------------------------------------------------------------------
# Email

EMAIL_HOST = envconfig('EMAIL_HOST')
EMAIL_HOST_USER = envconfig('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = envconfig('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(envconfig('EMAIL_PORT'))
EMAIL_USE_TLS = True  # envconfig('EMAIL_USE_TLS', True)
EMAIL_USE_SSL = False  # envconfig('EMAIL_USE_SSL', False)

# EMAIL_TIMEOUT = int(envconfig('EMAIL_TIMEOUT', 1000))
# EMAIL_SSL_KEYFILE = envconfig('EMAIL_SSL_KEYFILE', None)
# EMAIL_SSL_CERTFILE = envconfig('EMAIL_SSL_CERTFILE', None)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
