from django.urls import path

from pages.views import handler400
from pages.views import handler404
from pages.views import handler500

from .views import dev_view
from .views import dev_form
from .views import dev_coming_soon

app_name = 'dev'

urlpatterns = [
	path('', dev_view, name='dev'),
	path('form', dev_form, name='form'),
	path('coming-soon', dev_coming_soon, name='coming-soon'),
	path('400', handler400, name='400'),
	path('404', handler404, name='404'),
	path('500', handler500, name='500')
]
