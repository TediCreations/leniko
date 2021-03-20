from django.urls import path

from pages.views import handler400
from pages.views import handler404
from pages.views import handler500

from .views import DevView
from .views import TestView
from .views import CommingSoonView
from .views import PayView

app_name = 'dev'

urlpatterns = [
	path('', DevView.as_view(), name='dev'),
	path('pay', PayView.as_view(), name='pay'),
	path('test', TestView.as_view(), name='test'),
	path('coming-soon', CommingSoonView.as_view(), name='coming-soon'),
	path('400', handler400, name='400'),
	path('404', handler404, name='404'),
	path('500', handler500, name='500')
]
