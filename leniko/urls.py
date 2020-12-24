"""leniko URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls    import path
from django.urls    import include


from django.conf import settings
from django.conf.urls.static import static

from pages.views import home_view
from pages.views import about_view
from pages.views import contact_view

from pages.views import dev_view
from pages.views import dev_form
from pages.views import handler400
from pages.views import handler404
from pages.views import handler500

urlpatterns = [
	path(''         , home_view            , name='home'),

	path('product/' , include('products.urls')),

	path('about'    , about_view           , name='about'),
	path('contact'  , contact_view         , name='contact'),
	path('admin/'   , admin.site.urls      , name='admin'),

	path('dev/'     , dev_view             , name='dev'),
	path('dev/form' , dev_form             , name='dev'),
	path('dev/400'  , handler400           , name='dev'),
	path('dev/404'  , handler404           , name='dev'),
	path('dev/500'  , handler500           , name='dev'),
]

handler400 = 'pages.views.handler400'
handler404 = 'pages.views.handler404'
handler500 = 'pages.views.handler500'

if settings.DEBUG is True:
	import debug_toolbar
	urlpatterns.append(path('debug/' , include(debug_toolbar.urls)))

if settings.DEBUG is True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Admin page title
admin.site.site_header = "Leniko Jewelry";

#Modify Site Header
admin.site.index_title = 'Leniko Jewelry'
#Modify Site Title
admin.site.site_title = 'Administration'
