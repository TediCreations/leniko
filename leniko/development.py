from .base import *

# ------------------------------------------------------------------------------
# Debug

DEBUG = True

# ------------------------------------------------------------------------------
# Hosts

ALLOWED_HOSTS = envconfig("ALLOWED_HOSTS", "localhost").split()

# ------------------------------------------------------------------------------
# Static files

# Django will serve static files
INSTALLED_APPS.append('django.contrib.staticfiles')

# ------------------------------------------------------------------------------
# Debug Toolbar

INSTALLED_APPS.append('debug_toolbar')
INSTALLED_APPS.append('template_timings_panel')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ('127.0.0.1')

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
	'template_timings_panel.panels.TemplateTimings.TemplateTimings',
]

# No need to load jquery again
DEBUG_TOOLBAR_CONFIG = {
	'JQUERY_URL': '',
}
